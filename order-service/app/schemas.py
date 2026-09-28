from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    customer_id: int
    menu_item_id: int
    quantity: int = Field(gt=0)


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    menu_item_id: int
    quantity: int
    total_price: float
    status: str

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
