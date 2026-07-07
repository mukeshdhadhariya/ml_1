from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    age = Column(Integer)
    department = Column(Integer)
    job_role = Column(Integer)
    monthly_income = Column(Integer)
    total_working_years = Column(Integer)
    years_at_company = Column(Integer)
    overtime = Column(Integer)

    prediction = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)