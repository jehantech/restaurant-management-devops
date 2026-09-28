import os
import httpx

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

from .database import get_db
from .models import Order
from .schemas import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate
)

load_dotenv()

CUSTOMER_SERVICE_URL = os.getenv(
    "CUSTOMER_SERVICE_URL",
    "http://localhost:8003"
)

MENU_SERVICE_URL = os.getenv(
    "MENU_SERVICE_URL",
    "http://localhost:8002"
)
router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

VALID_STATUSES = [
    "PLACED",
    "PREPARING",
    "READY",
    "DELIVERED",
    "CANCELLED"
]


@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    # --------------------------------
    # Check Customer Service
    # --------------------------------

    try:
        customer_response = httpx.get(
            f"{CUSTOMER_SERVICE_URL}/customers/{order.customer_id}",
            timeout=5
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Customer Service is unavailable"
        )

    if customer_response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if customer_response.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail="Unable to verify customer"
        )

    # --------------------------------
    # Check Menu Service
    # --------------------------------

    try:
        menu_response = httpx.get(
            f"{MENU_SERVICE_URL}/{order.menu_item_id}",
            timeout=5
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Menu Service is unavailable"
        )

    if menu_response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    if menu_response.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail="Unable to verify menu item"
        )

    menu_item = menu_response.json()

    # --------------------------------
    # Calculate total price
    # --------------------------------

    total_price = menu_item["price"] * order.quantity

    # --------------------------------
    # Create Order
    # --------------------------------

    new_order = Order(
        customer_id=order.customer_id,
        menu_item_id=order.menu_item_id,
        quantity=order.quantity,
        total_price=total_price,
        status="PLACED"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if status_data.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Use one of: {VALID_STATUSES}"
        )

    order.status = status_data.status

    db.commit()
    db.refresh(order)

    return order


@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully"
    }
