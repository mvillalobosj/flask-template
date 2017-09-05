from flask import current_app

from app.models.user import User
from app.utilities.http import APIError, SC


def serialize_user(user):
    return dict(
        id=user.id,
        fname=user.fname,
        lname=user.lname,
        created=user.created
    )


class UserController:

    @staticmethod
    def get_user(user_id):
        user = current_app.db.query(User).get(user_id)
        if not user:
            raise APIError("User not found", SC.NOT_FOUND)
        return serialize_user(user)

    @staticmethod
    def search_users(fname):
        users = current_app.db.query(User).filter(User.fname == fname).all()
        return users

    @staticmethod
    def add_user(fname, lname):
        user = User(fname=fname, lname=lname)
        current_app.db.add(user)
        current_app.db.commit()
        return serialize_user(user)
