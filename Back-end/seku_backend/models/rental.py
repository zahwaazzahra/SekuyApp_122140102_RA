from sqlalchemy import Column, String, BigInteger, Date, Integer, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .meta import Base

class Rental(Base):
    __tablename__ = 'rentals'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    bike_id = Column(BigInteger, ForeignKey('bikes.id'), nullable=False)
    rental_date = Column(Date, nullable=False)
    duration_days = Column(Integer, nullable=False, default=1)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    ticket_id = Column(String(255), unique=True)
    status = Column(String(50), nullable=False, default='pending')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="rentals")
    bike = relationship("Bike", back_populates="rentals")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "bike_id": self.bike_id,
            "rental_date": str(self.rental_date),
            "duration_days": self.duration_days,
            "total_amount": float(self.total_amount),
            "payment_method": self.payment_method,
            "ticket_id": self.ticket_id,
            "status": self.status,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Rental(ticket_id='{self.ticket_id}', status='{self.status}')>"
