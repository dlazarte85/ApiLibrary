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
        return f"User(id={self.id}, username={self.username}, name={self.name}, email={self.email}, enabled={self.enable})"
