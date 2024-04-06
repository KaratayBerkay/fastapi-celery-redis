from pydantic import BaseModel
from typing import Optional


class DeviceCreateRequest(BaseModel):
    device_name: str
    device_type: str
    device_model: str
    device_status: str
    device_location: Optional[str] = None
