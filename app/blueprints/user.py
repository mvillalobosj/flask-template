from flask import Blueprint
from flask_apispec import doc, marshal_with, use_kwargs

from app.controllers.user import UserController
from app.schema.response import (
    AddUserResponse, UserGetResponse, UserSearchResponse)
from app.schema.request import AddUserRequest, UserSearchRequest

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route('/<int:id>', methods=['GET'])
@marshal_with(UserGetResponse)
@doc()
def get_user(id):
    user = UserController.get_user(id)
    return(dict(user=user))


@user_blueprint.route('/', methods=['POST'])
@use_kwargs(AddUserRequest)
@marshal_with(AddUserResponse)
@doc()
def add_user(fname, lname):
    user = UserController.add_user(fname, lname)
    return(dict(user=user))


@user_blueprint.route('/search', methods=['GET'])
@use_kwargs(UserSearchRequest)
@marshal_with(UserSearchResponse)
@doc()
def search_fname(fname):
    users = UserController.search_users(fname)
    return(dict(users=users))
