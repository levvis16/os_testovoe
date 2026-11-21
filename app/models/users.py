from sqlalchemy import ForeignKey, String, Integer
from database.database import Base
class User(Base):
    __tablename__ = "users"

    name
    phone
    booking_date
    booking_time
    guests
