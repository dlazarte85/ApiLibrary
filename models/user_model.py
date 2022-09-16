from sqlalchemy import Column, Integer, String, Boolean
from models import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=255), nullable=False)
    name = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False)
    password = Column(String(length=255), nullable=False)
    enabled = Column(Boolean, default=True)

    def __repr__(self):
        return f"User(id={self.id}, " \
               f"username={self.username}, " \
               f"name={self.name}, " \
               f"email={self.email}, " \
               f"enabled={self.enabled})"
