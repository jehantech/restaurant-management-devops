from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    address: str
    phone: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantResponse(RestaurantBase):
    id: int

    class Config:
        from_attributes = True