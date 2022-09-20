from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from models import Base
from sqlalchemy.orm import relationship


class ProductModel(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False, index=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    enabled = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="products")
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("CategoryModel", back_populates="products")

    def __repr__(self):
        return f"Product(" \
               f"id={self.id}, " \
               f"category_id={self.category_id}, " \
               f"name={self.name}, " \
               f"price={self.price}, " \
               f"stock={self.stock}, " \
               f"enabled={self.enabled}, " \
               f"deleted={self.deleted}, " \
               f"category={self.category})"
