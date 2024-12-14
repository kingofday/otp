from marshmallow import fields
from marshmallow.validate import OneOf
from wazo_confd.helpers.mallow import BaseSchema
from marshmallow import fields

class OtpRequestSchema(BaseSchema):
    id = fields.Str(dump_only=True)
    tenant_uuid = fields.Str(dump_only=True)
    application_uuid = fields.Str(dump_only=True)
    number = fields.Str(required=True)
    caller_id_name = fields.Str(required=True)
    caller_id_number = fields.Str(required=True)
    language = fields.Str(required=True)
    type = fields.String(validate=OneOf(['sound', 'digits','number','characters','ring','recording']), allow_none=False)
    value = fields.Str(required=True)
    status = fields.Str(required=True)
    creation_time = fields.Date()
    talking_to = fields.Dict(required=False) 
