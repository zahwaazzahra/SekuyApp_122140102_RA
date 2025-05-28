from sqlalchemy import Column, String, Text, DECIMAL, BigInteger, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .meta import Base

class Bike(Base):
    __tablename__ = 'bikes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    thumbnail = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    rentals = relationship("Rental", back_populates="bike")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": float(self.price),
            "thumbnail": self.thumbnail,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Bike(title='{self.title}', price='{self.price}')>"
