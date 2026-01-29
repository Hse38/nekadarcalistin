from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    analyses = relationship("Analysis", back_populates="employee", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Employee(id={self.id}, name={self.name}, surname={self.surname})>"


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    year = Column(Integer, nullable=False)
    
    # Working rules (required input)
    daily_working_hours = Column(Float, nullable=False)  # e.g., 9
    weekly_working_days = Column(Float, nullable=False)  # e.g., 5.5
    
    # Leave data (manual - HR controlled)
    annual_leave_total = Column(Float, nullable=False, default=0)
    annual_leave_used = Column(Float, nullable=False, default=0)
    extra_leave_days = Column(Float, nullable=False, default=0)  # mazeret izni etc.
    
    # Holiday data (JSON array of holiday objects)
    # Each holiday: {name, date, worked}
    holidays_data = Column(JSON, nullable=True)
    
    # Attendance data (JSON array of attendance records)
    # Each record: {date, check_in, check_out, hours}
    attendance_data = Column(JSON, nullable=True)
    
    # Calculated results (stored for quick retrieval and PDF)
    theoretical_working_days = Column(Float, nullable=True)
    actual_working_days = Column(Float, nullable=True)
    theoretical_working_hours = Column(Float, nullable=True)
    actual_working_hours = Column(Float, nullable=True)
    difference_hours = Column(Float, nullable=True)
    
    # Calendar data (JSON for yearly calendar view)
    calendar_data = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    employee = relationship("Employee", back_populates="analyses")

    def __repr__(self):
        return f"<Analysis(id={self.id}, employee_id={self.employee_id}, year={self.year})>"
