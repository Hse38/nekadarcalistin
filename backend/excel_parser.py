"""
Excel Parser for Attendance Data
Parses Excel files containing employee attendance records.
"""
import pandas as pd
from datetime import datetime, time
from typing import List, Dict, Optional


def parse_attendance_excel(file_path: str) -> List[Dict[str, any]]:
    """
    Parse attendance Excel file and return structured data.
    
    Expected format:
    - Column 1: Date (any recognizable date format)
    - Column 2: Check-in Time (time format)
    - Column 3: Check-out Time (time format)
    
    Additional columns are ignored.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        List of attendance records with date, check_in, check_out, and hours
        
    Raises:
        ValueError: If file format is invalid
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        if df.empty:
            raise ValueError("Excel file is empty")
        
        # Ensure we have at least 3 columns
        if len(df.columns) < 3:
            raise ValueError("Excel file must have at least 3 columns: Date, Check-in Time, Check-out Time")
        
        # Use first 3 columns regardless of header names
        date_col = df.columns[0]
        checkin_col = df.columns[1]
        checkout_col = df.columns[2]
        
        attendance_records = []
        
        for idx, row in df.iterrows():
            try:
                # Parse date
                date_value = row[date_col]
                if pd.isna(date_value):
                    continue  # Skip empty rows
                
                # Convert to datetime if not already
                if isinstance(date_value, str):
                    parsed_date = pd.to_datetime(date_value, errors='coerce')
                elif isinstance(date_value, (datetime, pd.Timestamp)):
                    parsed_date = date_value
                else:
                    continue
                
                if pd.isna(parsed_date):
                    continue
                
                # Format date as YYYY-MM-DD
                date_str = parsed_date.strftime('%Y-%m-%d')
                
                # Parse check-in time
                checkin_value = row[checkin_col]
                if pd.isna(checkin_value):
                    continue
                
                checkin_time = parse_time_value(checkin_value)
                if not checkin_time:
                    continue
                
                # Parse check-out time
                checkout_value = row[checkout_col]
                if pd.isna(checkout_value):
                    continue
                
                checkout_time = parse_time_value(checkout_value)
                if not checkout_time:
                    continue
                
                # Calculate hours worked
                hours = calculate_hours(checkin_time, checkout_time)
                
                attendance_records.append({
                    "date": date_str,
                    "check_in": checkin_time,
                    "check_out": checkout_time,
                    "hours": round(hours, 2)
                })
                
            except Exception as e:
                # Skip problematic rows
                continue
        
        if not attendance_records:
            raise ValueError("No valid attendance records found in Excel file")
        
        return attendance_records
        
    except Exception as e:
        raise ValueError(f"Error parsing Excel file: {str(e)}")


def parse_time_value(value) -> Optional[str]:
    """
    Parse various time formats and return HH:MM string.
    
    Args:
        value: Time value from Excel (can be string, time, datetime, or float)
        
    Returns:
        Time string in HH:MM format or None if invalid
    """
    try:
        # If it's already a time object
        if isinstance(value, time):
            return value.strftime('%H:%M')
        
        # If it's a datetime or timestamp
        if isinstance(value, (datetime, pd.Timestamp)):
            return value.strftime('%H:%M')
        
        # If it's a string
        if isinstance(value, str):
            # Try to parse various time formats
            for fmt in ['%H:%M', '%H:%M:%S', '%I:%M %p', '%I:%M:%S %p']:
                try:
                    parsed_time = datetime.strptime(value.strip(), fmt)
                    return parsed_time.strftime('%H:%M')
                except:
                    continue
        
        # If it's a float (Excel time as fraction of day)
        if isinstance(value, (float, int)):
            total_seconds = int(value * 24 * 3600)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        
        return None
        
    except:
        return None


def calculate_hours(check_in: str, check_out: str) -> float:
    """
    Calculate hours between check-in and check-out times.
    
    Args:
        check_in: Check-in time in HH:MM format
        check_out: Check-out time in HH:MM format
        
    Returns:
        Hours worked as float
    """
    try:
        checkin_time = datetime.strptime(check_in, '%H:%M')
        checkout_time = datetime.strptime(check_out, '%H:%M')
        
        # Handle overnight shifts (checkout before checkin)
        if checkout_time < checkin_time:
            checkout_time = checkout_time.replace(day=checkin_time.day + 1)
        
        diff = checkout_time - checkin_time
        hours = diff.total_seconds() / 3600
        
        return hours
        
    except:
        return 0.0


def validate_excel_file(file_path: str) -> Dict[str, any]:
    """
    Validate Excel file format without full parsing.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        Dictionary with validation results
    """
    try:
        df = pd.read_excel(file_path)
        
        if df.empty:
            return {
                "valid": False,
                "error": "Excel file is empty"
            }
        
        if len(df.columns) < 3:
            return {
                "valid": False,
                "error": "Excel file must have at least 3 columns"
            }
        
        # Count non-empty rows
        non_empty_rows = len(df.dropna(how='all'))
        
        return {
            "valid": True,
            "rows": non_empty_rows,
            "columns": len(df.columns)
        }
        
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


def parse_excel_attendance(file_content: bytes, year: int, filename: str = "attendance.xlsx") -> Dict:
    """
    Parse attendance Excel file from bytes content.
    
    Args:
        file_content: Excel file as bytes
        year: Year to filter records
        filename: Original filename for format detection
        
    Returns:
        Dictionary with records, total_days, total_hours, and monthly breakdown
    """
    from io import BytesIO
    
    try:
        buffer = BytesIO(file_content)
        
        if filename.endswith('.csv'):
            df = pd.read_csv(buffer)
        else:
            df = pd.read_excel(buffer)
        
        if df.empty:
            raise ValueError("Excel dosyası boş")
        
        if len(df.columns) < 3:
            raise ValueError("Excel dosyasında en az 3 sütun olmalı: Tarih, Giriş Saati, Çıkış Saati")
        
        date_col = df.columns[0]
        checkin_col = df.columns[1]
        checkout_col = df.columns[2]
        
        records = []
        monthly_data = {}
        total_hours = 0.0
        
        for idx, row in df.iterrows():
            try:
                date_value = row[date_col]
                if pd.isna(date_value):
                    continue
                
                # Parse date
                if isinstance(date_value, str):
                    parsed_date = pd.to_datetime(date_value, errors='coerce')
                elif isinstance(date_value, (datetime, pd.Timestamp)):
                    parsed_date = date_value
                else:
                    parsed_date = pd.to_datetime(date_value, errors='coerce')
                
                if pd.isna(parsed_date):
                    continue
                
                # Filter by year
                if parsed_date.year != year:
                    continue
                
                date_str = parsed_date.strftime('%Y-%m-%d')
                month = parsed_date.month
                
                # Parse times
                checkin_value = row[checkin_col]
                checkout_value = row[checkout_col]
                
                if pd.isna(checkin_value) or pd.isna(checkout_value):
                    continue
                
                checkin_time = parse_time_value(checkin_value)
                checkout_time = parse_time_value(checkout_value)
                
                if not checkin_time or not checkout_time:
                    continue
                
                hours = calculate_hours(checkin_time, checkout_time)
                
                if hours <= 0:
                    continue
                
                records.append({
                    "date": date_str,
                    "check_in": checkin_time,
                    "check_out": checkout_time,
                    "hours": round(hours, 2),
                    "month": month
                })
                
                # Update monthly breakdown
                if month not in monthly_data:
                    monthly_data[month] = {"days": 0, "hours": 0.0}
                monthly_data[month]["days"] += 1
                monthly_data[month]["hours"] += hours
                
                total_hours += hours
                
            except Exception:
                continue
        
        if not records:
            raise ValueError("Excel dosyasından geçerli kayıt okunamadı")
        
        return {
            "records": records,
            "total_days": len(records),
            "total_hours": round(total_hours, 2),
            "monthly_breakdown": monthly_data
        }
        
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Excel dosyası işlenirken hata: {str(e)}")
