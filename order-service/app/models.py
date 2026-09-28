from sqlalchemy import Column, Integer, Float, String
from .database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, nullable=False)

    menu_item_id = Column(Integer, nullable=False)

    quantity = Column(Integer, nullable=False)

    total_price = Column(Float, nullable=False)

    status = Column(
        String,
        default="PLACED",
        nullable=False
    )
