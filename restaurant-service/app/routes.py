from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Restaurant
from .schemas import RestaurantCreate, RestaurantResponse

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


@router.post("/", response_model=RestaurantResponse)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db)
):
    new_restaurant = Restaurant(
        name=restaurant.name,
        address=restaurant.address,
        phone=restaurant.phone
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


@router.get("/", response_model=list[RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    restaurant.name = restaurant_data.name
    restaurant.address = restaurant_data.address
    restaurant.phone = restaurant_data.phone

    db.commit()
    db.refresh(restaurant)

    return restaurant


@router.delete("/{restaurant_id}")
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    db.delete(restaurant)
    db.commit()

    return {
        "message": "Restaurant deleted successfully"
    }
