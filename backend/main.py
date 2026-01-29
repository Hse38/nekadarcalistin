"""
HR Working Time Analysis System - Main API Application
"""
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import json
import os

from database import SessionLocal, engine, Base
from models import Employee, Analysis
from config import settings
from calculation_service import WorkingTimeCalculator
from excel_parser import parse_excel_attendance
from pdf_service import generate_analysis_pdf
from holidays_data import TURKEY_HOLIDAYS

# Create tables
Base.metadata.create_all(bind=engine)

# Create directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)

app = FastAPI(
    title="HR Çalışma Süresi Analiz Sistemi",
    description="Çalışan çalışma sürelerini analiz eden profesyonel HR sistemi",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== EMPLOYEE ENDPOINTS ====================

@app.get("/api/employees")
def get_employees(db: Session = Depends(get_db)):
    """Get all employees"""
    employees = db.query(Employee).all()
    return {
        "employees": [
            {
                "id": e.id,
                "name": e.name,
                "surname": e.surname,
                "created_at": e.created_at.isoformat() if e.created_at else None
            }
            for e in employees
        ],
        "total": len(employees)
    }


@app.post("/api/employees")
def create_employee(
    name: str = Form(...),
    surname: str = Form(...),
    db: Session = Depends(get_db)
):
    """Create a new employee"""
    employee = Employee(name=name, surname=surname)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return {
        "id": employee.id,
        "name": employee.name,
        "surname": employee.surname,
        "created_at": employee.created_at.isoformat() if employee.created_at else None
    }


@app.get("/api/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get employee by ID"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
    return {
        "id": employee.id,
        "name": employee.name,
        "surname": employee.surname,
        "created_at": employee.created_at.isoformat() if employee.created_at else None
    }


@app.delete("/api/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete an employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
    db.delete(employee)
    db.commit()
    return {"message": "Çalışan silindi"}


# ==================== HOLIDAY ENDPOINTS ====================

@app.get("/api/holidays/{year}")
def get_holidays(year: int):
    """Get Turkey official holidays for a year"""
    if year not in TURKEY_HOLIDAYS:
        return {"holidays": [], "total": 0}
    
    holidays = TURKEY_HOLIDAYS[year]
    return {
        "holidays": [
            {
                "id": i + 1,
                "name": h["name"],
                "date": h["date"],
                "type": h.get("type", "national"),
                "worked": False
            }
            for i, h in enumerate(holidays)
        ],
        "total": len(holidays)
    }


# ==================== ANALYSIS ENDPOINTS ====================

@app.post("/api/analyses")
async def create_analysis(
    employee_id: int = Form(...),
    year: int = Form(...),
    daily_working_hours: float = Form(...),
    weekly_working_days: float = Form(...),
    annual_leave_total: float = Form(0),
    annual_leave_used: float = Form(0),
    extra_leave_days: float = Form(0),
    holidays_data: str = Form("[]"),
    attendance_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Create a new analysis for an employee"""
    
    # Validate employee exists
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
    
    # Validate working rules
    if daily_working_hours <= 0 or daily_working_hours > 24:
        raise HTTPException(status_code=400, detail="Günlük çalışma saati 0-24 arası olmalı")
    if weekly_working_days <= 0 or weekly_working_days > 7:
        raise HTTPException(status_code=400, detail="Haftalık çalışma günü 0-7 arası olmalı")
    
    # Parse holidays data
    try:
        holidays_list = json.loads(holidays_data)
    except json.JSONDecodeError:
        holidays_list = []
    
    # Calculate holidays not worked
    holidays_not_worked = sum(1 for h in holidays_list if not h.get("worked", False))
    
    # Initialize calculator
    calculator = WorkingTimeCalculator(
        year=year,
        daily_working_hours=daily_working_hours,
        weekly_working_days=weekly_working_days
    )
    
    # Calculate theoretical working days
    theoretical_days = calculator.calculate_theoretical_working_days(
        annual_leave_used=annual_leave_used,
        extra_leave_days=extra_leave_days,
        holidays_not_worked=holidays_not_worked
    )
    
    # Calculate theoretical working hours
    theoretical_hours = calculator.calculate_theoretical_working_hours(theoretical_days)
    
    # Parse attendance file if provided
    attendance_data = None
    actual_days = None
    actual_hours = None
    
    if attendance_file and attendance_file.filename:
        try:
            content = await attendance_file.read()
            attendance_data = parse_excel_attendance(content, year, attendance_file.filename)
            actual_days = attendance_data["total_days"]
            actual_hours = attendance_data["total_hours"]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Excel dosyası işlenemedi: {str(e)}")
    
    # Calculate difference
    difference_hours = None
    if actual_hours is not None:
        difference_hours = actual_hours - theoretical_hours
    
    # Generate calendar data
    calendar_data = calculator.generate_calendar_data(
        holidays_list=holidays_list,
        attendance_records=attendance_data.get("records", []) if attendance_data else []
    )
    
    # Create analysis record
    analysis = Analysis(
        employee_id=employee_id,
        year=year,
        daily_working_hours=daily_working_hours,
        weekly_working_days=weekly_working_days,
        annual_leave_total=annual_leave_total,
        annual_leave_used=annual_leave_used,
        extra_leave_days=extra_leave_days,
        holidays_data=holidays_list,
        attendance_data=attendance_data,
        theoretical_working_days=theoretical_days,
        actual_working_days=actual_days,
        theoretical_working_hours=theoretical_hours,
        actual_working_hours=actual_hours,
        difference_hours=difference_hours,
        calendar_data=calendar_data
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return format_analysis_response(analysis, employee)


@app.get("/api/analyses")
def get_analyses(
    employee_id: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all analyses with optional filters"""
    query = db.query(Analysis)
    
    if employee_id:
        query = query.filter(Analysis.employee_id == employee_id)
    if year:
        query = query.filter(Analysis.year == year)
    
    analyses = query.order_by(Analysis.created_at.desc()).all()
    
    result = []
    for analysis in analyses:
        employee = db.query(Employee).filter(Employee.id == analysis.employee_id).first()
        if employee:
            result.append(format_analysis_response(analysis, employee))
    
    return {"analyses": result, "total": len(result)}


@app.get("/api/analyses/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Get analysis by ID"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadı")
    
    employee = db.query(Employee).filter(Employee.id == analysis.employee_id).first()
    return format_analysis_response(analysis, employee)


@app.get("/api/analyses/{analysis_id}/pdf")
def download_analysis_pdf(analysis_id: int, db: Session = Depends(get_db)):
    """Generate and download PDF report"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadı")
    
    employee = db.query(Employee).filter(Employee.id == analysis.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
    
    # Generate PDF
    pdf_bytes = generate_analysis_pdf(analysis, employee)
    
    filename = f"analiz_{employee.surname}_{employee.name}_{analysis.year}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.delete("/api/analyses/{analysis_id}")
def delete_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Delete an analysis"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadı")
    
    db.delete(analysis)
    db.commit()
    return {"message": "Analiz silindi"}


def format_analysis_response(analysis: Analysis, employee: Employee) -> dict:
    """Format analysis response"""
    
    # Calculate monthly breakdown
    monthly_breakdown = []
    if analysis.calendar_data:
        for month in range(1, 13):
            month_data = analysis.calendar_data.get(str(month), {})
            monthly_breakdown.append({
                "month": month,
                "month_name": get_month_name(month),
                "theoretical_days": month_data.get("theoretical_days", 0),
                "theoretical_hours": month_data.get("theoretical_hours", 0),
                "actual_days": month_data.get("actual_days"),
                "actual_hours": month_data.get("actual_hours"),
                "difference_hours": month_data.get("difference_hours")
            })
    
    return {
        "id": analysis.id,
        "employee_id": analysis.employee_id,
        "employee_name": employee.name,
        "employee_surname": employee.surname,
        "year": analysis.year,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
        
        # Working rules
        "daily_working_hours": analysis.daily_working_hours,
        "weekly_working_days": analysis.weekly_working_days,
        
        # Leave data
        "annual_leave_total": analysis.annual_leave_total,
        "annual_leave_used": analysis.annual_leave_used,
        "extra_leave_days": analysis.extra_leave_days,
        
        # Holiday data
        "holidays_data": analysis.holidays_data or [],
        "holidays_worked": sum(1 for h in (analysis.holidays_data or []) if h.get("worked", False)),
        "holidays_not_worked": sum(1 for h in (analysis.holidays_data or []) if not h.get("worked", False)),
        
        # Calculated results
        "theoretical_working_days": analysis.theoretical_working_days,
        "actual_working_days": analysis.actual_working_days,
        "theoretical_working_hours": analysis.theoretical_working_hours,
        "actual_working_hours": analysis.actual_working_hours,
        "hours_difference": analysis.difference_hours,
        
        # Status
        "has_attendance_data": analysis.actual_working_days is not None,
        "is_overtime": (analysis.difference_hours or 0) > 0,
        "is_missing_hours": (analysis.difference_hours or 0) < 0,
        
        # Monthly breakdown
        "monthly_breakdown": monthly_breakdown,
        
        # Calendar data
        "calendar_data": analysis.calendar_data
    }


def get_month_name(month: int) -> str:
    """Get Turkish month name"""
    months = {
        1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
        5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
        9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
    }
    return months.get(month, "")


@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "HR Çalışma Süresi Analiz Sistemi API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
