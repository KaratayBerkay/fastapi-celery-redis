from pydantic import BaseModel


class DeviceCreateResponse(BaseModel):
    device_id: str
    device_name: str
    device_type: str
    device_model: str
    device_location: str
    device_status: str

