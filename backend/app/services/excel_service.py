"""
Excel Parsing Service

Parses attendance Excel files and extracts working time data.
"""
import pandas as pd
from io import BytesIO
from datetime import datetime, date, time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


class ExcelParseError(Exception):
    """Exception raised when Excel parsing fails."""
    pass


@dataclass
class AttendanceData:
    """Parsed attendance data from Excel."""
    records: List[Dict[str, Any]] = field(default_factory=list)
    total_days: int = 0
    total_hours: float = 0.0
    monthly_breakdown: Dict[int, Dict[str, float]] = field(default_factory=dict)


def parse_time(time_value: Any) -> Optional[str]:
    """Parse time from various formats to HH:MM string."""
    if pd.isna(time_value):
        return None
    
    if isinstance(time_value, time):
        return time_value.strftime("%H:%M")
    
    if isinstance(time_value, datetime):
        return time_value.strftime("%H:%M")
    
    if isinstance(time_value, str):
        # Try common formats
        for fmt in ["%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M:%S %p"]:
            try:
                parsed = datetime.strptime(time_value.strip(), fmt)
                return parsed.strftime("%H:%M")
            except ValueError:
                continue
        return None
    
    return None


def parse_date(date_value: Any, year: int) -> Optional[date]:
    """Parse date from various formats."""
    if pd.isna(date_value):
        return None
    
    if isinstance(date_value, date):
        return date_value
    
    if isinstance(date_value, datetime):
        return date_value.date()
    
    if isinstance(date_value, str):
        # Try common formats
        for fmt in ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]:
            try:
                parsed = datetime.strptime(date_value.strip(), fmt)
                return parsed.date()
            except ValueError:
                continue
        return None
    
    return None


def calculate_hours(check_in: str, check_out: str) -> float:
    """Calculate hours worked from check-in and check-out times."""
    try:
        in_time = datetime.strptime(check_in, "%H:%M")
        out_time = datetime.strptime(check_out, "%H:%M")
        
        # Handle overnight shifts
        if out_time < in_time:
            # Add 24 hours to out_time
            from datetime import timedelta
            out_time = out_time + timedelta(hours=24)
        
        diff = out_time - in_time
        hours = diff.total_seconds() / 3600
        
        return round(hours, 2)
    except (ValueError, TypeError):
        return 0.0


def parse_attendance_excel(
    file_content: bytes,
    year: int,
    filename: str = "attendance.xlsx"
) -> AttendanceData:
    """
    Parse attendance Excel file.
    
    Expected format:
    Date | Check-in Time | Check-out Time
    
    Args:
        file_content: Excel file content as bytes
        year: Year for validation
        filename: Original filename for format detection
    
    Returns:
        AttendanceData with parsed records
    
    Raises:
        ExcelParseError: If parsing fails
    """
    try:
        # Read Excel file
        buffer = BytesIO(file_content)
        
        # Determine file type
        if filename.endswith('.csv'):
            df = pd.read_csv(buffer)
        else:
            df = pd.read_excel(buffer)
        
        if df.empty:
            raise ExcelParseError("Excel dosyası boş")
        
        # Try to identify columns
        # Look for date, check-in, check-out columns
        columns = df.columns.tolist()
        
        date_col = None
        checkin_col = None
        checkout_col = None
        
        # Common column name patterns
        date_patterns = ['date', 'tarih', 'gün', 'gun', 'day']
        checkin_patterns = ['check-in', 'checkin', 'giriş', 'giris', 'in', 'başlangıç', 'start']
        checkout_patterns = ['check-out', 'checkout', 'çıkış', 'cikis', 'out', 'bitiş', 'end']
        
        for i, col in enumerate(columns):
            col_lower = str(col).lower().strip()
            
            if date_col is None:
                for pattern in date_patterns:
                    if pattern in col_lower:
                        date_col = i
                        break
            
            if checkin_col is None:
                for pattern in checkin_patterns:
                    if pattern in col_lower:
                        checkin_col = i
                        break
            
            if checkout_col is None:
                for pattern in checkout_patterns:
                    if pattern in col_lower:
                        checkout_col = i
                        break
        
        # If columns not found by name, use position (first 3 columns)
        if date_col is None:
            date_col = 0
        if checkin_col is None:
            checkin_col = 1
        if checkout_col is None:
            checkout_col = 2
        
        # Parse records
        records = []
        monthly_data: Dict[int, Dict[str, float]] = {}
        total_hours = 0.0
        
        for idx, row in df.iterrows():
            try:
                # Get values by column index
                date_val = row.iloc[date_col]
                checkin_val = row.iloc[checkin_col]
                checkout_val = row.iloc[checkout_col]
                
                # Parse date
                record_date = parse_date(date_val, year)
                if record_date is None:
                    continue
                
                # Skip if year doesn't match
                if record_date.year != year:
                    continue
                
                # Parse times
                checkin_time = parse_time(checkin_val)
                checkout_time = parse_time(checkout_val)
                
                if checkin_time is None or checkout_time is None:
                    continue
                
                # Calculate hours
                hours = calculate_hours(checkin_time, checkout_time)
                
                if hours <= 0:
                    continue
                
                # Add record
                month = record_date.month
                records.append({
                    'date': record_date,
                    'check_in_time': checkin_time,
                    'check_out_time': checkout_time,
                    'hours_worked': hours,
                    'month': month
                })
                
                # Update monthly breakdown
                if month not in monthly_data:
                    monthly_data[month] = {'days': 0, 'hours': 0.0}
                monthly_data[month]['days'] += 1
                monthly_data[month]['hours'] += hours
                
                total_hours += hours
                
            except Exception as e:
                # Skip problematic rows
                continue
        
        if not records:
            raise ExcelParseError("Excel dosyasından geçerli kayıt okunamadı")
        
        return AttendanceData(
            records=records,
            total_days=len(records),
            total_hours=round(total_hours, 2),
            monthly_breakdown=monthly_data
        )
        
    except ExcelParseError:
        raise
    except Exception as e:
        raise ExcelParseError(f"Excel dosyası işlenirken hata: {str(e)}")
