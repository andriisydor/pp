from flask import request, jsonify, Blueprint
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import NoResultFound
from marshmallow import ValidationError
from schemas import UserSchema, SongSchema, PlaylistSchema
from models import Session, User, Playlist, Song, playlist_song
from config import app

# authentication
from flask_httpauth import HTTPBasicAuth
from access import check_user_by_id, check_user_by_found

api = Blueprint('api', __name__)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    session = Session()
    user_data = session.query(User).filter_by(username=username).first()
    if user_data and bcrypt.check_password_hash(user_data.password, password):
        return username


@auth.error_handler
def auth_error(status):
    return "Access Denied", status


# admin-user
@auth.get_user_roles
def get_user_roles(user):
    return user


@api.route("/song", methods=["POST"])
@auth.login_required(role='admin')
def create_song():
    session = Session()

    json_data = request.get_json()
    if not json_data:
        return {"message": "Input data is empty"}, 400

    try:
        song_data = SongSchema().load(json_data)
    except ValidationError as err:
        return err.messages, 422

    song = Song(**song_data)

    exists = session.query(Song).filter_by(name=json_data['name']).first()
    if exists:
        return {"message": "Song with this name exists"}, 400

    session.add(song)
    session.commit()

    return jsonify(SongSchema().dump(song))


@api.route("/song/<int:song_id>", methods=["GET"])
@auth.login_required
def get_song(song_id):
    session = Session()
    try:
        song = session.query(Song).filter_by(id=song_id).one()
    except NoResultFound:
        return {"message": "Song with this id does not exist."}, 400
    return jsonify(SongSchema().dump(song))


@api.route("/song/<int:song_id>", methods=["PUT"])
@auth.login_required(role='admin')
def update_song(song_id):
    session = Session()
    json_data = request.get_json()

    try:
        song = session.query(Song).filter_by(id=song_id).one()
    except NoResultFound:
        return {"message": "Song with this id does not exist."}, 400

    # checking if suitable new name
    exists = None
    if "name" in json_data:
        exists = session.query(Song).filter_by(name=json_data["name"]).first()
        # checking if found song is the same we want to change
        if exists and exists.id == song_id:
            exists = None
    if exists:
        return {"message": "Song with this name exists"}, 400

    attributes = Song.__dict__.keys()

    # updating
    for key, value in json_data.items():
        if key == 'id':
            return {"message": "You can not change id"}, 403

        if key not in attributes:
            return {"message": "Invalid input data provided"}, 404

        setattr(song, key, value)

    session.commit()

    song = session.query(Song).filter_by(id=song_id).first()

    return jsonify(SongSchema().dump(song))


@api.route("/song/<int:song_id>", methods=["DELETE"])
@auth.login_required(role='admin')
def delete_song(song_id):
    session = Session()
    try:
        song = session.query(Song).filter_by(id=song_id).one()
    except NoResultFound:
        return {"message": "Song with this id does not exist."}, 400

    exists = session.query(playlist_song).filter_by(song_id=song_id).all()
    if exists:
        return {"message": "Cannot delete song because it exists in playlists."}, 403

    session.delete(song)
    session.commit()
    return {"message": "Successfully deleted song."}


@api.route("/playlist", methods=["POST"])
@auth.login_required
def create_playlist():
    session = Session()

    json_data = request.get_json()
    if not json_data:
        return {"message": "Input data is empty"}, 400

    try:
        playlist_data = PlaylistSchema().load(json_data)
    except ValidationError as err:
        return err.messages, 422

    playlist = Playlist(**playlist_data)

    exists = session.query(Playlist).filter_by(title=json_data['title']).first()
    if exists and exists.user_id == playlist_data["user_id"]:
        return {"message": "Playlist with this name exists"}, 400

    user_data = session.query(User).filter_by(id=json_data["user_id"]).first()
    if not user_data:
        return {"message": "User with this id does not exist"}, 400

    # authentication
    authentication = check_user_by_found(user_data, auth.current_user())
    if authentication:
        return authentication

    session.add(playlist)
    session.commit()

    return jsonify(PlaylistSchema().dump(playlist))


@api.route("/playlist/<int:playlist_id>", methods=["GET"])
@auth.login_required
def get_playlist(playlist_id):
    session = Session()
    try:
        playlist = session.query(Playlist).filter_by(id=playlist_id).one()
    except NoResultFound:
        return {"message": "Playlist with this id does not exist."}, 400

    # authentication
    authentication = check_user_by_id(session, playlist.user_id, auth.current_user())
    if authentication and playlist.private:
        return authentication

    return jsonify(PlaylistSchema().dump(playlist))


@api.route("/playlist/<int:playlist_id>", methods=["PUT"])
@auth.login_required
def update_playlist(playlist_id):
    session = Session()
    json_data = request.get_json()

    try:
        playlist = session.query(Playlist).filter_by(id=playlist_id).one()
    except NoResultFound:
        return {"message": "Playlist with this id does not exist."}, 400

    # authentication
    authentication = check_user_by_id(session, playlist.user_id, auth.current_user())
    if authentication and playlist.private:
        return authentication

    # not let other change your public playlist to private
    if authentication and "private" in json_data and not playlist.private:
        return authentication

    # checking if suitable new user_id
    if "user_id" in json_data:
        return {"message": f"You can not change the owner"}, 403

    # exists = None
    # if "user_id" in json_data:
    #     exists = session.query(User).filter_by(id=json_data["user_id"]).first()
    # if not exists:
    #     return {"message": f"User with this id does not exist"}, 400

    # checking if suitable new title
    exists = None
    if "title" in json_data:
        exists = session.query(Playlist).filter_by(title=json_data["title"]).first()
        # checking if found user is the same we want to change
        if exists and exists.id == playlist_id:
            exists = None
    if exists:
        return {"message": f"User with id = {exists.user_id} already has a playlist with the same title"}, 400

    attributes = Playlist.__dict__.keys()

    # updating
    for key, value in json_data.items():
        if key == 'id':
            return {"message": "You can not change id"}, 403
        if key == 'songs':
            return {"message": "You can not change songs"}, 403
        if key not in attributes:
            return {"message": "Invalid input data provided"}, 404

        setattr(playlist, key, value)

    session.commit()

    playlist = session.query(Playlist).filter_by(id=playlist_id).first()

    return jsonify(PlaylistSchema().dump(playlist))


@api.route("/playlist/<int:playlist_id>", methods=["DELETE"])
@auth.login_required
def delete_playlist(playlist_id):
    session = Session()
    try:
        playlist = session.query(Playlist).filter_by(id=playlist_id).one()
    except NoResultFound:
        return {"message": "Playlist with this id does not exist."}, 400

    # authentication
    authentication = check_user_by_id(session, playlist.user_id, auth.current_user())
    if authentication:
        return authentication

    session.delete(playlist)
    session.commit()
    return {"message": "Successfully deleted playlist."}


@api.route("/playlist/song/<int:song_id>", methods=["PUT"])
@auth.login_required
def add_song_to_playlist(song_id):
    session = Session()
    json_data = request.get_json()

    if not json_data:
        return {"message": "Input data is empty"}, 400

    playlist_data = PlaylistSchema().load(json_data)
    playlist_id = playlist_data["id"]

    try:
        song = session.query(Song).filter_by(id=song_id).one()
    except NoResultFound:
        return {"message": "Song with this id does not exist."}, 400

    try:
        playlist = session.query(Playlist).filter_by(id=playlist_id).one()
    except NoResultFound:
        return {"message": "Playlist with this id does not exist."}, 400

    # authentication
    authentication = check_user_by_id(session, playlist.user_id, auth.current_user())
    if authentication and playlist.private:
        return authentication

    playlist_dict = playlist.__dict__
    playlist_dict["songs"].append(song)
    session.commit()

    return jsonify(PlaylistSchema().dump(playlist))


@api.route("/playlist/song/<int:song_id>", methods=["DELETE"])
@auth.login_required
def delete_song_from_playlist(song_id):
    session = Session()
    json_data = request.get_json()
    if not json_data:
        return {"message": "Input data is empty"}, 400

    playlist_data = PlaylistSchema().load(json_data)
    playlist_id = playlist_data["id"]
    try:
        song = session.query(Song).filter_by(id=song_id).one()
    except NoResultFound:
        return {"message": "Song with this id does not exist."}, 400

    try:
        exists = session.query(playlist_song).filter_by(playlist_id=playlist_id).all()
    except NoResultFound:
        return {"message": "Playlist with this id does not exist."}, 400

    try:
        playlist = session.query(Playlist).filter_by(id=playlist_id).one()
    except NoResultFound:
        return {"message": "Playlist with this id does not exist."}, 400

    # authentication
    authentication = check_user_by_id(session, playlist.user_id, auth.current_user())
    if authentication and playlist.private:
        return authentication

    playlist_dict = playlist.__dict__

    if song not in playlist_dict["songs"]:
        return {"message": f"Song with this id does not exist in playlist with id = {playlist_id}."}, 400

    playlist_dict["songs"].remove(song)

    session.commit()
    return {"message": f"Successfully deleted song from playlist with id = {playlist_id}."}


@api.route("/service", methods=["GET"])
@auth.login_required
def get_service_playlists():
    session = Session()
    playlists = session.query(Playlist).filter_by(private='0').all()
    if not playlists:
        return {"message": "There are no playlists"}, 400
    schema = PlaylistSchema(many=True)
    return jsonify(schema.dump(playlists))


@api.route("/service/<int:playlist_id>", methods=["GET"])
@auth.login_required
def get_service_playlist_by_id(playlist_id):
    session = Session()
    try:
        playlist = session.query(Playlist).filter_by(id=playlist_id).one()
    except NoResultFound:
        return {"message": "Playlist with this id does not exist."}, 400

    # authentication
    if playlist.private:
        authentication = check_user_by_id(session, playlist.user_id, auth.current_user())
        if authentication:
            return authentication

    return jsonify(PlaylistSchema().dump(playlist))


@api.route("/service/user/<int:user_id>", methods=["GET"])
@auth.login_required
def get_service_playlists_by_user_id(user_id):
    session = Session()
    try:
        private_playlists = session.query(Playlist).filter_by(user_id=user_id, private="1").all()
        if session.query(User).filter_by(id=user_id).first():
            public_playlists = session.query(Playlist).filter_by(private="0").all()
        else:
            return {"message": "User with this id does not exist."}, 400
    except NoResultFound:
        return {"message": "Playlist with this id does not exist."}, 400

    # authentication
    authentication = check_user_by_id(session, user_id, auth.current_user())
    if authentication:
        return authentication

    schema = PlaylistSchema(many=True)
    return jsonify(schema.dump(private_playlists + public_playlists))


@api.route("/user", methods=["POST"])
def create_user():
    session = Session()

    json_data = request.get_json()
    if not json_data:
        return {"message": "Input data is empty"}, 400

    try:
        user_data = UserSchema().load(json_data)
    except ValidationError as err:
        return err.messages, 422

    user_data.update(password=bcrypt.generate_password_hash(json_data['password']).decode('utf-8'))
    user = User(**user_data)

    exists = session.query(User).filter_by(username=json_data['username']).first()
    if exists:
        return {"message": "User with this username exists"}, 400
    exists = session.query(User).filter_by(email=json_data['email']).first()
    if exists:
        return {"message": "User with this email exists"}, 400

    session.add(user)
    session.commit()

    return jsonify(UserSchema().dump(user))


@api.route("/user/<int:user_id>", methods=["PUT"])
@auth.login_required
def update_user(user_id):
    session = Session()
    json_data = request.get_json()

    try:
        user = session.query(User).filter_by(id=user_id).one()
    except NoResultFound:
        return {"message": "User with this id does not exist."}, 400

    # authentication of user
    authentication = check_user_by_found(user, auth.current_user())
    if authentication:
        return authentication

    # checking if suitable new username
    exists = None
    if "username" in json_data:
        exists = session.query(User).filter_by(username=json_data["username"]).first()
        # checking if found user is the same we want to change
        if exists and exists.id == user_id:
            exists = None
    if exists:
        return {"message": "User with this username exists"}, 400

    # checking if suitable new email
    if "email" in json_data:
        exists = session.query(User).filter_by(email=json_data["email"]).first()
        # checking if found user is the same we want to change
        if exists and exists.id == user_id:
            exists = None
    if exists:
        return {"message": "User with this email exists"}, 400

    attributes = User.__dict__.keys()

    # updating
    for key, value in json_data.items():
        if key == 'id':
            return {"message": "You can not change id"}, 403

        if key not in attributes:
            return {"message": "Invalid input data provided"}, 404

        if key == 'password':
            value = Bcrypt().generate_password_hash(value).decode('utf-8')

        setattr(user, key, value)

    session.commit()

    user = session.query(User).filter_by(id=user_id).first()

    return jsonify(UserSchema().dump(user))


@api.route("/user/<int:user_id>", methods=["DELETE"])
@auth.login_required
def delete_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).one()
    except NoResultFound:
        return {"message": "User with this id does not exist."}, 400

    # authentication of user
    authentication = check_user_by_found(user, auth.current_user())
    if authentication:
        return authentication

    # .all() -> .first()
    # user -> playlist
    playlist = session.query(Playlist).filter_by(user_id=user_id).first()
    if playlist:
        return {"message": "Cannot delete user because it has playlists."}, 403

    session.delete(user)
    session.commit()
    return {"message": "Successfully deleted user."}


# if __name__ == "__main__":
#     # db.create_all()
#     api.run(debug=True, port=5000)
