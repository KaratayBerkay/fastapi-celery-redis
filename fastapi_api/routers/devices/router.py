from fastapi.routing import APIRouter
from validations import DeviceCreateRequest, DeviceCreateResponse

from models import Devices


devices_route = APIRouter(prefix="/devices", tags=["Devices"])
devices_route.include_router(devices_route, include_in_schema=False)


@devices_route.post("/create", response_model=DeviceCreateResponse, description="Aygıt olustur")
def devices_create(device: DeviceCreateRequest):
    found_device: Devices = Devices.filter(Devices.device_name == device.device_name).first()

    if found_device:
        raise Exception("Cihaz zaten kayıtlı.")
    new_device = Devices(
        device_name=device.device_name,
        device_type=device.device_type,
        device_model=device.device_model,
        device_last_location=device.device_location,
        device_status=device.device_status
    )

    new_device.save()

    return DeviceCreateResponse(
        device_id=str(new_device.device_id),
        device_name=new_device.device_name,
        device_type=new_device.device_type,
        device_model=new_device.device_model,
        device_location=new_device.device_last_location,
        device_status=new_device.device_status
    )


@devices_route.delete("/{device_id}", description="Aygıt sil")
def devices_delete(device_id: str):
    found_device: Devices = Devices.filter(Devices.device_id == device_id).first()

    if not found_device:
        raise Exception("Cihaz bulunamadı.")

    device = DeviceCreateResponse(
        device_id=str(found_device.device_id),
        device_name=found_device.device_name,
        device_type=found_device.device_type,
        device_model=found_device.device_model,
        device_location=found_device.device_last_location,
        device_status=found_device.device_status
    )

    found_device.delete()

    return {
        "message": "Cihaz silindi.",
        "device": device
    }


@devices_route.get("/{query}", description="Aygıt bilgisi")
def devices_info(query: str):
    parsed_queries, query_args = query.split("&"), []
    page, limit = 1, 10
    for parsed_query in parsed_queries:
        key, val = parsed_query.split("=")
        if key == "page":
            page = int(val)
        elif key == "limit":
            limit = int(val)
        elif getattr(Devices, key):
            query_args.append(getattr(Devices, key) == val)

    print('query_args', query_args)
    found_devices: list = Devices.filter(*query_args).limit(limit).offset((page - 1) * limit).all()

    if not found_devices:
        raise Exception("Cihaz bulunamadı.")

    return {
        "count": len(found_devices),
        "message": "Aygıt bilgisi",
        "devices": [DeviceCreateResponse(
            device_id=str(found_device.device_id),
            device_name=found_device.device_name,
            device_type=found_device.device_type,
            device_model=found_device.device_model,
            device_location=found_device.device_last_location,
            device_status=found_device.device_status
        ) for found_device in found_devices]
    }


@devices_route.get("/locations/{device_id}/history/", description="Konum geçmişi")
def devices_location_history(device_id: str, limit: int = 50):
    found_device: Devices = Devices.filter(Devices.device_id == device_id).first()

    if not found_device:
        raise Exception("Cihaz bulunamadı.")
    histories = sorted(
            [
                {
                    "history_id": str(history.history_id),
                    "created_at": history.created_at,
                    "device_location": history.device_location
                } for history in found_device.history
            ], key=lambda x: x["created_at"], reverse=True
        )[:limit]
    return {
        "message": "Konum geçmişi",
        "device": DeviceCreateResponse(
            device_id=str(found_device.device_id),
            device_name=found_device.device_name,
            device_type=found_device.device_type,
            device_model=found_device.device_model,
            device_location=found_device.device_last_location,
            device_status=found_device.device_status
        ),
        "count": len(histories),
        "history": histories
    }


@devices_route.get("/locations/last", description="Son konum bilgisi")
def devices_last_location():
    found_device: Devices = Devices.filter().order_by(Devices.created_at.desc()).all()

    if not found_device:
        raise Exception("Kayıtlı cihaz bulunamadı.")

    return {
        "count": len(found_device),
        "message": "Son konum bilgisi",
        "devices": [DeviceCreateResponse(
            device_id=str(found_device.device_id),
            device_name=found_device.device_name,
            device_type=found_device.device_type,
            device_model=found_device.device_model,
            device_location=found_device.device_last_location,
            device_status=found_device.device_status
        ) for found_device in found_device]
    }

