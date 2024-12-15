import logging

from flask import url_for, request
from wazo_confd.auth import required_acl
from .model import OtpRequestDto
from .schema import OtpRequestSchema

logger = logging.getLogger(__name__)
class OtpPlaybackResource:
    schema = OtpRequestSchema
    model = OtpRequestDto

    def build_headers(self, model):
        return {'Location': url_for('otp_request_playback', uuid=model.application_uuid, _external=True)}

    @required_acl('calld.otp.create')
    def post(self):
        form = self.schema().load(request.get_json())
        model = self.model(**form)
        model = self.service.process_otp_request(model)
        return self.schema().dump(model), 201, self.build_headers(model)