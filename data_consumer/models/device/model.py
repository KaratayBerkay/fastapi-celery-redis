from ..mixin import BaseMixin
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, UUID, text, ForeignKey
from typing import List


class Devices(BaseMixin):

    __tablename__ = "devices"

    device_id: Mapped[str] = mapped_column(
        UUID, nullable=False, server_default=text("gen_random_uuid()"), index=True, comment="Device ID"
    )
    device_name: Mapped[str] = mapped_column(String, nullable=False, comment="Device Name")
    device_type: Mapped[str] = mapped_column(String, comment="Device Type")
    device_model: Mapped[str] = mapped_column(String, comment="Device Model")
    device_last_location: Mapped[str] = mapped_column(String, server_default="0,0", comment="Device Location")
    device_status: Mapped[str] = mapped_column(String, server_default="1", comment="Device Status")

    history: Mapped[List["DevicesHistory"]] = relationship(
        "DevicesHistory", back_populates="device", foreign_keys="DevicesHistory.device_id"
    )


class DevicesHistory(BaseMixin):

    __tablename__ = "devices_history"

    history_id: Mapped[str] = mapped_column(
        UUID, nullable=False, server_default=text("gen_random_uuid()"), index=True, comment="Device ID"
    )
    device_location: Mapped[str] = mapped_column(String, server_default="0,0", comment="Device Location")

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False, comment="Device ID")

    device: Mapped["Devices"] = relationship(
        "Devices", back_populates="history", foreign_keys=[device_id]
    )




