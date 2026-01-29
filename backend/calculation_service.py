"""
Calculation Service
Core business logic for HR working time analysis.
All calculations follow strict business rules.
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from calendar import monthrange


def calculate_analysis(
    year: int,
    daily_working_hours: float,
    weekly_working_days: float,
    annual_leave_used: float,
    extra_leave_days: float,
    holidays_data: List[Dict],
    attendance_data: Optional[List[Dict]] = None
) -> Dict:
    """
    Perform complete working time analysis for a single year.
    
    This is the core calculation engine following strict business rules:
    - Year-based analysis only
    - 5.5 day work week (Mon-Fri full, Sat half, Sun off)
    - Leave and holidays reduce theoretical working days
    - Actual data comes from Excel attendance records
    
    Args:
        year: Analysis year
        daily_working_hours: Daily working hours (e.g., 9)
        weekly_working_days: Weekly working days (e.g., 5.5)
        annual_leave_used: Annual leave days used
        extra_leave_days: Extra leave days (mazeret izni)
        holidays_data: List of holidays with {name, date, worked} flags
        attendance_data: Optional list of attendance records from Excel
        
    Returns:
        Dictionary with all calculated results and calendar data
    """
    
    # 1. Calculate possible working days (based on 5.5-day week)
    possible_working_days = calculate_possible_working_days(year, weekly_working_days)
    
    # 2. Calculate holidays not worked
    holidays_not_worked = sum(1 for h in holidays_data if not h.get('worked', False))
    
    # 3. Calculate theoretical working days
    # Start with all possible working days, subtract leave and holidays not worked
    theoretical_working_days = (
        possible_working_days 
        - annual_leave_used 
        - extra_leave_days 
        - holidays_not_worked
    )
    
    # 4. Calculate theoretical working hours
    theoretical_working_hours = theoretical_working_days * daily_working_hours
    
    # 5. Calculate actual working days and hours from attendance data
    actual_working_days = 0
    actual_working_hours = 0.0
    
    if attendance_data:
        actual_working_days = len(attendance_data)
        actual_working_hours = sum(record['hours'] for record in attendance_data)
    
    # 6. Calculate difference
    difference_hours = actual_working_hours - theoretical_working_hours
    
    # 7. Generate calendar data
    calendar_data = generate_calendar_data(
        year=year,
        weekly_working_days=weekly_working_days,
        annual_leave_used=annual_leave_used,
        extra_leave_days=extra_leave_days,
        holidays_data=holidays_data,
        attendance_data=attendance_data or []
    )
    
    return {
        "theoretical_working_days": round(theoretical_working_days, 2),
        "actual_working_days": actual_working_days,
        "theoretical_working_hours": round(theoretical_working_hours, 2),
        "actual_working_hours": round(actual_working_hours, 2),
        "difference_hours": round(difference_hours, 2),
        "calendar_data": calendar_data,
        "metadata": {
            "possible_working_days": round(possible_working_days, 2),
            "holidays_not_worked": holidays_not_worked,
            "holidays_worked": len(holidays_data) - holidays_not_worked,
            "total_holidays": len(holidays_data),
            "annual_leave_used": annual_leave_used,
            "extra_leave_days": extra_leave_days
        }
    }


def calculate_possible_working_days(year: int, weekly_working_days: float) -> float:
    """
    Calculate possible working days in a year based on weekly working pattern.
    
    For 5.5 day week:
    - Monday-Friday: full days (1.0 each)
    - Saturday: half day (0.5)
    - Sunday: non-working (0)
    
    Args:
        year: The year to calculate
        weekly_working_days: Weekly working days (e.g., 5.5)
        
    Returns:
        Total possible working days in the year
    """
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    
    total_days = 0.0
    current_date = start_date
    
    while current_date <= end_date:
        weekday = current_date.weekday()  # 0=Monday, 6=Sunday
        
        if weekly_working_days == 5.5:
            # Standard Turkish work week
            if weekday <= 4:  # Monday to Friday
                total_days += 1.0
            elif weekday == 5:  # Saturday
                total_days += 0.5
            # Sunday = 0
        elif weekly_working_days == 5.0:
            # 5-day work week (Mon-Fri only)
            if weekday <= 4:
                total_days += 1.0
        elif weekly_working_days == 6.0:
            # 6-day work week (Mon-Sat)
            if weekday <= 5:
                total_days += 1.0
        else:
            # Custom work week - distribute evenly
            if weekday < int(weekly_working_days):
                total_days += 1.0
            elif weekday == int(weekly_working_days) and (weekly_working_days % 1) > 0:
                total_days += (weekly_working_days % 1)
        
        current_date += timedelta(days=1)
    
    return total_days


def generate_calendar_data(
    year: int,
    weekly_working_days: float,
    annual_leave_used: float,
    extra_leave_days: float,
    holidays_data: List[Dict],
    attendance_data: List[Dict]
) -> Dict:
    """
    Generate calendar data for the entire year with day-by-day status.
    
    Day State Priority (STRICT ORDER):
    1. Worked (from Excel attendance)
    2. Leave (annual or extra)
    3. Official Holiday
    4. Weekend
    5. Missing (expected workday but not worked)
    
    Args:
        year: Analysis year
        weekly_working_days: Weekly working days pattern
        annual_leave_used: Annual leave days used
        extra_leave_days: Extra leave days
        holidays_data: Holiday information
        attendance_data: Attendance records
        
    Returns:
        Dictionary with monthly calendar data
    """
    
    # Create lookup sets for quick access
    worked_dates = {record['date'] for record in attendance_data}
    holiday_map = {h['date']: h for h in holidays_data}
    
    # Note: We don't have specific leave dates, so we'll mark them as "leave pool"
    # In a real system, HR would provide specific leave dates
    total_leave_days = annual_leave_used + extra_leave_days
    
    calendar = {}
    
    for month in range(1, 13):
        month_name = datetime(year, month, 1).strftime('%B')
        days_in_month = monthrange(year, month)[1]
        
        month_data = {
            "month": month,
            "month_name": month_name,
            "days": [],
            "summary": {
                "worked": 0,
                "leave": 0,
                "holiday": 0,
                "holiday_worked": 0,
                "missing": 0,
                "weekend": 0
            }
        }
        
        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day)
            date_str = date.strftime('%Y-%m-%d')
            weekday = date.weekday()
            
            # Determine day status based on priority
            status = "unknown"
            hours = None
            note = ""
            
            # Priority 1: Worked (from Excel)
            if date_str in worked_dates:
                # Find the record
                record = next(r for r in attendance_data if r['date'] == date_str)
                hours = record['hours']
                
                # Check if it's also a holiday
                if date_str in holiday_map:
                    holiday = holiday_map[date_str]
                    status = "holiday_worked"
                    note = holiday['name']
                    month_data["summary"]["holiday_worked"] += 1
                else:
                    status = "worked"
                    month_data["summary"]["worked"] += 1
            
            # Priority 2: Leave (we don't have specific dates, just mark as potential)
            # This would need enhancement with actual leave date tracking
            
            # Priority 3: Official Holiday (not worked)
            elif date_str in holiday_map:
                holiday = holiday_map[date_str]
                if not holiday.get('worked', False):
                    status = "holiday"
                    note = holiday['name']
                    month_data["summary"]["holiday"] += 1
                else:
                    # Holiday but marked as worked (but no attendance data)
                    status = "holiday"
                    note = f"{holiday['name']} (marked as worked but no attendance)"
                    month_data["summary"]["holiday"] += 1
            
            # Priority 4: Weekend
            elif is_weekend(weekday, weekly_working_days):
                status = "weekend"
                month_data["summary"]["weekend"] += 1
            
            # Priority 5: Missing (should have worked but didn't)
            else:
                # This is a workday but no attendance record
                status = "missing"
                month_data["summary"]["missing"] += 1
            
            day_data = {
                "date": date_str,
                "day": day,
                "weekday": weekday,
                "weekday_name": date.strftime('%A'),
                "status": status,
                "hours": hours,
                "note": note
            }
            
            month_data["days"].append(day_data)
        
        calendar[month] = month_data
    
    return calendar


def is_weekend(weekday: int, weekly_working_days: float) -> bool:
    """
    Determine if a day is a weekend based on working pattern.
    
    Args:
        weekday: Day of week (0=Monday, 6=Sunday)
        weekly_working_days: Weekly working days pattern
        
    Returns:
        True if it's a weekend day
    """
    if weekly_working_days == 5.5:
        # Sunday is full weekend, Saturday is half (not considered weekend)
        return weekday == 6
    elif weekly_working_days == 5.0:
        # Saturday and Sunday are weekend
        return weekday >= 5
    elif weekly_working_days == 6.0:
        # Only Sunday is weekend
        return weekday == 6
    else:
        # Custom - assume last days are weekend
        return weekday >= int(weekly_working_days)


def get_monthly_distribution(calendar_data: Dict) -> Dict:
    """
    Get monthly distribution of work for charts.
    
    Args:
        calendar_data: Calendar data from generate_calendar_data
        
    Returns:
        Monthly distribution data
    """
    distribution = {}
    
    for month, data in calendar_data.items():
        distribution[month] = {
            "month_name": data["month_name"],
            "worked_days": data["summary"]["worked"],
            "worked_hours": sum(
                day["hours"] for day in data["days"] 
                if day["hours"] is not None
            )
        }
    
    return distribution


class WorkingTimeCalculator:
    """
    Calculator class for working time analysis.
    Provides a class-based interface for the calculation functions.
    """
    
    def __init__(self, year: int, daily_working_hours: float, weekly_working_days: float):
        self.year = year
        self.daily_working_hours = daily_working_hours
        self.weekly_working_days = weekly_working_days
    
    def calculate_theoretical_working_days(
        self,
        annual_leave_used: float = 0,
        extra_leave_days: float = 0,
        holidays_not_worked: int = 0
    ) -> float:
        """Calculate theoretical working days after deductions."""
        possible_days = calculate_possible_working_days(self.year, self.weekly_working_days)
        theoretical_days = possible_days - annual_leave_used - extra_leave_days - holidays_not_worked
        return round(max(0, theoretical_days), 2)
    
    def calculate_theoretical_working_hours(self, theoretical_days: float) -> float:
        """Calculate theoretical working hours."""
        return round(theoretical_days * self.daily_working_hours, 2)
    
    def generate_calendar_data(
        self,
        holidays_list: List[Dict],
        attendance_records: List[Dict]
    ) -> Dict:
        """Generate calendar data for the year."""
        return generate_calendar_data(
            year=self.year,
            weekly_working_days=self.weekly_working_days,
            annual_leave_used=0,
            extra_leave_days=0,
            holidays_data=holidays_list,
            attendance_data=attendance_records
        )

