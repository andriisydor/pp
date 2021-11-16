import datetime

from flask import Flask, request
from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load
from models import Session , User, Playlist,Song


##### SCHEMAS #####

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    email = fields.Str()


class SongSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    singer = fields.Str()
    album = fields.Str()
    duration = fields.Str()


class PlaylistSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    songs = fields.List(fields.Nested(SongSchema))
    user_id = fields.Int()
    private = fields.Bool()