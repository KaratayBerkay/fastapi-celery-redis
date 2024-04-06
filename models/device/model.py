from models.mixin import BaseMixin
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, UUID, text


class Devices(BaseMixin):

    __tablename__ = "devices"

    device_id: str = mapped_column(
        UUID, nullable=False, server_default=text("gen_random_uuid()"), index=True, comment="Device ID"
    )
    device_name: str = mapped_column(String, nullable=False, comment="Device Name")
    device_type: str = mapped_column(String, comment="Device Type")
    device_model: str = mapped_column(String, comment="Device Model")
    device_location: str = mapped_column(String, server_default="0,0", comment="Device Location")
    device_status: str = mapped_column(String, server_default="1", comment="Device Status")

