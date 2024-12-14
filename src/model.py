from sqlalchemy import (
    Column
)
from sqlalchemy import text
from sqlalchemy.types import (String,Date)
from xivo_dao.helpers.db_manager import UUIDAsString
from sqlalchemy.types import JSON

from ..db import Base


class OtpRequestModel(Base):
    __tablename__ = 'plugin_otp_playback_request'

    id = Column(String(128), primary_key=True, nullable=False)
    tenant_uuid = Column(UUIDAsString(36), nullable=False)
    application_uuid = Column(UUIDAsString(36), nullable=False)
    number = Column(String(128), nullable=False)
    caller_id_name = Column(String(128), nullable=False)
    caller_id_number = Column(String(128), nullable=False)
    language = Column(String(128), nullable=False)
    type = Column(String(128), nullable=False)
    value = Column(String(128), nullable=False)
    status = Column(String(128), nullable=False)
    creation_time = Column(Date, nullable=True)
    talking_to = Column(JSON, nullable=True) 
