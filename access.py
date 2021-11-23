from models import User


def check_user_by_id(session, user_id, given_username):
    found = session.query(User).filter_by(id=user_id).first()
    if found and found.username != given_username:
        return "Access Denied", 401
    elif not found:
        return {"message": "User with this id does not exist."}, 400


def check_user_by_found(found_user, given_username):
    if found_user.username != given_username:
        return "Access Denied", 401
