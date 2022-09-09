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
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("CategoryModel", back_populates="products")

    def __repr__(self):
        return f"Product(id={self.id}, category_id={self.category_id}, name={self.name}, price={self.price}, stock={self.stock}, enabled={self.enable}, deleted={self.deleted})"
