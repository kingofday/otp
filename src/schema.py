from marshmallow import fields, validates, ValidationError
from wazo_confd.helpers.mallow import BaseSchema


class OtpRequestSchema(BaseSchema):
    uuid = fields.Str(dump_only=True)
    call_id = fields.Str(dump_only=True)
    tenant_uuid = fields.Str(dump_only=True)
    application_uuid = fields.Str(dump_only=True)
    number = fields.Str(required=True)
    caller_id_name = fields.Str(required=True)
    caller_id_number = fields.Str(required=True)
    answered = fields.Boolean(required=True)
    language = fields.Str(required=True)
    status = fields.Str(required=True)
    creation_time = fields.Date()
    talking_to = fields.Dict(required=False)
    uris = fields.List(fields.Str(), required=False)

    @validates("uris")
    def validate_uris(self, uris):
        if not isinstance(uris, list):
            raise ValidationError("Uris must be a list of strings.")

        for uri in uris:
            if not isinstance(uri, str):
                raise ValidationError(f"Invalid entry in uris: {
                                      uri} is not a string.")

            # Split the string by ":"
            if ":" not in uri:
                raise ValidationError(f"Invalid uri format: '{
                                      uri}'. Missing ':' separator.")

            prefix, value = uri.split(":", 1)

            if prefix == "sound":
                if not value.isalpha():
                    raise ValidationError(f"Invalid 'sound' value: '{
                                          value}' must be a string.")
            elif prefix == "digits":
                if not value.isdigit():
                    raise ValidationError(f"Invalid 'digits' value: '{
                                          value}' must be a number.")
            else:
                raise ValidationError(f"Invalid uri prefix: '{
                                      prefix}'. Expected 'sound' or 'digits'.")
