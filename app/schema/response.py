from marshmallow import fields, Schema


class UserResponse(Schema):
    id = fields.Integer()
    fname = fields.String()
    lname = fields.String()
    created = fields.String()


class UserGetResponse(Schema):
    user = fields.Nested(UserResponse)


class AddUserResponse(Schema):
    user = fields.Nested(UserResponse)


class UserSearchResponse(Schema):
    users = fields.Nested(UserResponse, many=True)
