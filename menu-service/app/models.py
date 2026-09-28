from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    name = Column(String, nullable=False)

    category = Column(String, nullable=False)

    price = Column(Float, nullable=False)

    available = Column(Boolean, default=True)
