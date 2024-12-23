import logging
from functools import wraps

from ari.exceptions import ARIException, ARIHTTPError
from flask_restful import Resource
from xivo import mallow_helpers, rest_api_helpers
from xivo.flask.auth_verifier import AuthVerifierFlask
from .exceptions import AsteriskARIError, AsteriskARIUnreachable


from flask import url_for, request
from wazo_confd.auth import required_acl
from wazo_calld.http import AuthResource
from .model import OtpRequestDto
from .schema import OtpRequestSchema

auth_verifier = AuthVerifierFlask()
logger = logging.getLogger(__name__)

def handle_ari_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ARIHTTPError as e:
            raise AsteriskARIError(
                {'base_url': e.client.base_url}, e.original_error, e.original_message
            )
        except ARIException as e:
            raise AsteriskARIUnreachable(
                {'base_url': e.client.base_url}, e.original_error, e.original_message
            )

    return wrapper


class ErrorCatchingResource(Resource):
    method_decorators = [
        mallow_helpers.handle_validation_exception,
        handle_ari_exception,
        rest_api_helpers.handle_api_exception,
    ] + Resource.method_decorators

class OtpPlaybackResource(ErrorCatchingResource):
    schema = OtpRequestSchema
    model = OtpRequestDto

    def build_headers(self, model):
        return {'Location': url_for('otp_request_playback', uuid=model.application_uuid, _external=True)}

    @required_acl('workano.otp.request')
    def post(self):
        form = self.schema().load(request.get_json())
        model = self.model(**form)
        model = self.service.process_otp_request(model)
        return self.schema().dump(model), 201, self.build_headers(model)