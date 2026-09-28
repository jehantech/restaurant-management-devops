import os
import httpx

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import MenuItem
from .schemas import MenuItemCreate, MenuItemResponse

load_dotenv()

router = APIRouter()

RESTAURANT_SERVICE_URL = os.getenv(
    "RESTAURANT_SERVICE_URL",
    "http://localhost:8001"
)

@router.post("/", response_model=MenuItemResponse)
def create_menu_item(
    item: MenuItemCreate,
    db: Session = Depends(get_db)
):

    # Check whether restaurant exists
    try:
        response = httpx.get(
            f"{RESTAURANT_SERVICE_URL}/restaurants/{item.restaurant_id}",
            timeout=5
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Restaurant Service is unavailable"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail="Unable to verify restaurant"
        )

    # Create menu item
    new_item = MenuItem(
        restaurant_id=item.restaurant_id,
        name=item.name,
        category=item.category,
        price=item.price,
        available=item.available
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get("/", response_model=list[MenuItemResponse])
def get_menu_items(
    db: Session = Depends(get_db)
):
    return db.query(MenuItem).all()


@router.get("/{item_id}", response_model=MenuItemResponse)
def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    return item


@router.put("/{item_id}", response_model=MenuItemResponse)
def update_menu_item(
    item_id: int,
    item_data: MenuItemCreate,
    db: Session = Depends(get_db)
):

    # Verify restaurant exists
    try:
        response = httpx.get(
            f"{RESTAURANT_SERVICE_URL}/restaurants/{item_data.restaurant_id}",
            timeout=5
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Restaurant Service is unavailable"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    item.restaurant_id = item_data.restaurant_id
    item.name = item_data.name
    item.category = item_data.category
    item.price = item_data.price
    item.available = item_data.available

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{item_id}")
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Menu item deleted successfully"
    }
