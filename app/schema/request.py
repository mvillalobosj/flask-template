from marshmallow import fields, Schema


class AddUserRequest(Schema):
    fname = fields.String()
    lname = fields.String()


class UserSearchRequest(Schema):
    fname = fields.String()
