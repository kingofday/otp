import logging
from wazo_calld_client import Client as CalldClient
from wazo_auth_client import Client as AuthClient
from wazo_confd_client import Client as ConfdClient

logger = logging.getLogger(__name__)

class Plugin:
    def load(self, dependencies):
        logger.info('otp playback plugin loading')
        api = dependencies['api']
        config = dependencies['config']
        auth_client = AuthClient(**config['auth'])
        calld_client = CalldClient(host='127.0.0.1', port=443, verify_certificate=False, https=True)
        confd_client = ConfdClient(host='127.0.0.1', port=443, verify_certificate=False, https=True)
        init_db('postgresql://asterisk:proformatique@localhost/asterisk?application_name=wazo-power_dialer-plugin')
        campaign_service = build_campaign_service(auth_client, calld_client, confd_client)
        contact_service = build_contact_service()
        contact_list_service = build_contact_list_service()
        contact_contact_list_service = build_contact_contact_list_service()
        campaign_contact_list_service = build_campaign_contact_list_service()
        campaign_contact_call_service = build_campaign_contact_call_service()
        bus_consumer = dependencies['bus_consumer']
        bus_event_handler = CampaignBusEventHandler(campaign_service)

        # Subscribe to bus events
        bus_event_handler.subscribe(bus_consumer)

        # Campaigns
        api.add_resource(
            CampaignListResource,
            '/powerdialer/campaigns',
            resource_class_args=(campaign_service,)
        )

    def unload(self):
        pass
