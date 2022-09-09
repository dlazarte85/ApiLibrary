from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user_model import UserModel
from .category_model import CategoryModel
from .product_model import ProductModel
