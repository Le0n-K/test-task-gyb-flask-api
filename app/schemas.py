from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
