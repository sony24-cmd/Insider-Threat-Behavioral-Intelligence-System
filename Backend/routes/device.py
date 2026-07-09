from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse
from services import device_service

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.post("/", response_model=DeviceResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return device_service.create_device(db, device)


@router.get("/", response_model=list[DeviceResponse])
def get_all_devices(db: Session = Depends(get_db)):
    return device_service.get_all_devices(db)


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db)
):
    updated_device = device_service.update_device(db, device_id, device)

    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")

    return updated_device


@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    deleted_device = device_service.delete_device(db, device_id)

    if not deleted_device:
        raise HTTPException(status_code=404, detail="Device not found")

    return {"message": "Device deleted successfully"}