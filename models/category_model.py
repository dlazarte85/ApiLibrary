from sqlalchemy import Column, Integer, String, Boolean
from models import Base
from sqlalchemy.orm import relationship


class CategoryModel(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False, unique=True, index=True)
    enabled = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)

    products = relationship("ProductModel", back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, enabled={self.enable}, deleted={self.deleted})"
