from pydantic import BaseModel, Field


class MenuItemBase(BaseModel):
    restaurant_id: int
    name: str
    category: str
    price: float = Field(gt=0)
    available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        from_attributes = True
