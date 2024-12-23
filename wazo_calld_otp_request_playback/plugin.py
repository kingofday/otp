import logging
from wazo_calld_client import Client as CalldClient
from wazo_auth_client import Client as AuthClient
from wazo_confd_client import Client as ConfdClient
from .db import init_db
from .services import build_otp_playback_service
from bus_consume import OtpRequestBusEventHandler
from .resource import OtpPlaybackResource
logger = logging.getLogger(__name__)

class Plugin:
    def load(self, dependencies):
        logger.info('otp playback plugin loading')
        api = dependencies['api']
        config = dependencies['config']
        auth_client = AuthClient(**config['auth'])
        calld_client = CalldClient(host='127.0.0.1', port=443, verify_certificate=False, https=True)
        confd_client = ConfdClient(host='127.0.0.1', port=443, verify_certificate=False, https=True)
        init_db('postgresql://asterisk:proformatique@localhost/asterisk?application_name=workano-otp-playback-plugin')
        otp_request_service = build_otp_playback_service(auth_client, calld_client, confd_client)
        bus_consumer = dependencies['bus_consumer']
        bus_event_handler = OtpRequestBusEventHandler(otp_request_service)

        # Subscribe to bus events
        bus_event_handler.subscribe(bus_consumer)

        # Campaigns
        api.add_resource(
            OtpPlaybackResource,
            '/otp-playback',
            resource_class_args=(otp_request_service,)
        )

    def unload(self):
        pass
