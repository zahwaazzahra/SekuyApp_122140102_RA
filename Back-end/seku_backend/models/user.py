from sqlalchemy import Column, String, BigInteger, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .meta import Base
from passlib.hash import pbkdf2_sha256

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    rentals = relationship("Rental", back_populates="user")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password_plain_text):
        self.password_hash = pbkdf2_sha256.hash(password_plain_text)

    def check_password(self, password_plain_text):
        return pbkdf2_sha256.verify(password_plain_text, self.password_hash)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
        }

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
