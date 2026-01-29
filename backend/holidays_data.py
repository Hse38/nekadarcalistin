"""
Turkey Official Holidays Data
This module provides official Turkish holidays for different years.
"""
from datetime import date
from typing import List, Dict


def get_turkey_holidays(year: int) -> List[Dict[str, any]]:
    """
    Returns official Turkish holidays for a given year.
    
    Args:
        year: The year to get holidays for
        
    Returns:
        List of holiday dictionaries with 'name' and 'date' keys
    """
    holidays = {
        2024: [
            {"name": "Yılbaşı", "date": "2024-01-01"},
            {"name": "Ramazan Bayramı 1. Gün", "date": "2024-04-10"},
            {"name": "Ramazan Bayramı 2. Gün", "date": "2024-04-11"},
            {"name": "Ramazan Bayramı 3. Gün", "date": "2024-04-12"},
            {"name": "Ulusal Egemenlik ve Çocuk Bayramı", "date": "2024-04-23"},
            {"name": "Emek ve Dayanışma Günü", "date": "2024-05-01"},
            {"name": "Kurban Bayramı 1. Gün", "date": "2024-06-16"},
            {"name": "Kurban Bayramı 2. Gün", "date": "2024-06-17"},
            {"name": "Kurban Bayramı 3. Gün", "date": "2024-06-18"},
            {"name": "Kurban Bayramı 4. Gün", "date": "2024-06-19"},
            {"name": "Demokrasi ve Milli Birlik Günü", "date": "2024-07-15"},
            {"name": "Zafer Bayramı", "date": "2024-08-30"},
            {"name": "Cumhuriyet Bayramı", "date": "2024-10-29"},
        ],
        2025: [
            {"name": "Yılbaşı", "date": "2025-01-01"},
            {"name": "Ramazan Bayramı 1. Gün", "date": "2025-03-30"},
            {"name": "Ramazan Bayramı 2. Gün", "date": "2025-03-31"},
            {"name": "Ramazan Bayramı 3. Gün", "date": "2025-04-01"},
            {"name": "Ulusal Egemenlik ve Çocuk Bayramı", "date": "2025-04-23"},
            {"name": "Emek ve Dayanışma Günü", "date": "2025-05-01"},
            {"name": "Kurban Bayramı 1. Gün", "date": "2025-06-06"},
            {"name": "Kurban Bayramı 2. Gün", "date": "2025-06-07"},
            {"name": "Kurban Bayramı 3. Gün", "date": "2025-06-08"},
            {"name": "Kurban Bayramı 4. Gün", "date": "2025-06-09"},
            {"name": "Demokrasi ve Milli Birlik Günü", "date": "2025-07-15"},
            {"name": "Zafer Bayramı", "date": "2025-08-30"},
            {"name": "Cumhuriyet Bayramı", "date": "2025-10-29"},
        ],
        2026: [
            {"name": "Yılbaşı", "date": "2026-01-01"},
            {"name": "Ramazan Bayramı 1. Gün", "date": "2026-03-20"},
            {"name": "Ramazan Bayramı 2. Gün", "date": "2026-03-21"},
            {"name": "Ramazan Bayramı 3. Gün", "date": "2026-03-22"},
            {"name": "Ulusal Egemenlik ve Çocuk Bayramı", "date": "2026-04-23"},
            {"name": "Emek ve Dayanışma Günü", "date": "2026-05-01"},
            {"name": "Kurban Bayramı 1. Gün", "date": "2026-05-27"},
            {"name": "Kurban Bayramı 2. Gün", "date": "2026-05-28"},
            {"name": "Kurban Bayramı 3. Gün", "date": "2026-05-29"},
            {"name": "Kurban Bayramı 4. Gün", "date": "2026-05-30"},
            {"name": "Demokrasi ve Milli Birlik Günü", "date": "2026-07-15"},
            {"name": "Zafer Bayramı", "date": "2026-08-30"},
            {"name": "Cumhuriyet Bayramı", "date": "2026-10-29"},
        ],
        2023: [
            {"name": "Yılbaşı", "date": "2023-01-01"},
            {"name": "Ramazan Bayramı 1. Gün", "date": "2023-04-21"},
            {"name": "Ramazan Bayramı 2. Gün", "date": "2023-04-22"},
            {"name": "Ramazan Bayramı 3. Gün", "date": "2023-04-23"},
            {"name": "Ulusal Egemenlik ve Çocuk Bayramı", "date": "2023-04-23"},
            {"name": "Emek ve Dayanışma Günü", "date": "2023-05-01"},
            {"name": "Kurban Bayramı 1. Gün", "date": "2023-06-28"},
            {"name": "Kurban Bayramı 2. Gün", "date": "2023-06-29"},
            {"name": "Kurban Bayramı 3. Gün", "date": "2023-06-30"},
            {"name": "Kurban Bayramı 4. Gün", "date": "2023-07-01"},
            {"name": "Demokrasi ve Milli Birlik Günü", "date": "2023-07-15"},
            {"name": "Zafer Bayramı", "date": "2023-08-30"},
            {"name": "Cumhuriyet Bayramı 1. Gün", "date": "2023-10-29"},
        ],
        2022: [
            {"name": "Yılbaşı", "date": "2022-01-01"},
            {"name": "Ramazan Bayramı 1. Gün", "date": "2022-05-02"},
            {"name": "Ramazan Bayramı 2. Gün", "date": "2022-05-03"},
            {"name": "Ramazan Bayramı 3. Gün", "date": "2022-05-04"},
            {"name": "Ulusal Egemenlik ve Çocuk Bayramı", "date": "2022-04-23"},
            {"name": "Emek ve Dayanışma Günü", "date": "2022-05-01"},
            {"name": "Kurban Bayramı 1. Gün", "date": "2022-07-09"},
            {"name": "Kurban Bayramı 2. Gün", "date": "2022-07-10"},
            {"name": "Kurban Bayramı 3. Gün", "date": "2022-07-11"},
            {"name": "Kurban Bayramı 4. Gün", "date": "2022-07-12"},
            {"name": "Demokrasi ve Milli Birlik Günü", "date": "2022-07-15"},
            {"name": "Zafer Bayramı", "date": "2022-08-30"},
            {"name": "Cumhuriyet Bayramı", "date": "2022-10-29"},
        ],
    }
    
    return holidays.get(year, [])


def get_holiday_dates(year: int) -> set:
    """
    Returns a set of holiday dates for quick lookup.
    
    Args:
        year: The year to get holiday dates for
        
    Returns:
        Set of date strings in YYYY-MM-DD format
    """
    holidays = get_turkey_holidays(year)
    return {holiday["date"] for holiday in holidays}


# Direct dictionary access for quick lookups
TURKEY_HOLIDAYS = {
    2024: [
        {"name": "Yılbaşı", "date": "2024-01-01"},
        {"name": "Ramazan Bayramı 1. Gün", "date": "2024-04-10"},
        {"name": "Ramazan Bayramı 2. Gün", "date": "2024-04-11"},
        {"name": "Ramazan Bayramı 3. Gün", "date": "2024-04-12"},
        {"name": "Ulusal Egemenlik ve Çocuk Bayramı", "date": "2024-04-23"},
        {"name": "Emek ve Dayanışma Günü", "date": "2024-05-01"},
        {"name": "Kurban Bayramı 1. Gün", "date": "2024-06-16"},
        {"name": "Kurban Bayramı 2. Gün", "date": "2024-06-17"},
        {"name": "Kurban Bayramı 3. Gün", "date": "2024-06-18"},
        {"name": "Kurban Bayramı 4. Gün", "date": "2024-06-19"},
        {"name": "Demokrasi ve Milli Birlik Günü", "date": "2024-07-15"},
        {"name": "Zafer Bayramı", "date": "2024-08-30"},
        {"name": "Cumhuriyet Bayramı", "date": "2024-10-29"},
    ],
    2025: [
        {"name": "Yılbaşı", "date": "2025-01-01"},
        {"name": "Ramazan Bayramı 1. Gün", "date": "2025-03-30"},
        {"name": "Ramazan Bayramı 2. Gün", "date": "2025-03-31"},
        {"name": "Ramazan Bayramı 3. Gün", "date": "2025-04-01"},
        {"name": "Ulusal Egemenlik ve Çocuk Bayramı", "date": "2025-04-23"},
        {"name": "Emek ve Dayanışma Günü", "date": "2025-05-01"},
        {"name": "Kurban Bayramı 1. Gün", "date": "2025-06-06"},
        {"name": "Kurban Bayramı 2. Gün", "date": "2025-06-07"},
        {"name": "Kurban Bayramı 3. Gün", "date": "2025-06-08"},
        {"name": "Kurban Bayramı 4. Gün", "date": "2025-06-09"},
        {"name": "Demokrasi ve Milli Birlik Günü", "date": "2025-07-15"},
        {"name": "Zafer Bayramı", "date": "2025-08-30"},
        {"name": "Cumhuriyet Bayramı", "date": "2025-10-29"},
    ],
    2026: [
        {"name": "Yılbaşı", "date": "2026-01-01"},
        {"name": "Ramazan Bayramı 1. Gün", "date": "2026-03-20"},
        {"name": "Ramazan Bayramı 2. Gün", "date": "2026-03-21"},
        {"name": "Ramazan Bayramı 3. Gün", "date": "2026-03-22"},
        {"name": "Ulusal Egemenlik ve Çocuk Bayramı", "date": "2026-04-23"},
        {"name": "Emek ve Dayanışma Günü", "date": "2026-05-01"},
        {"name": "Kurban Bayramı 1. Gün", "date": "2026-05-27"},
        {"name": "Kurban Bayramı 2. Gün", "date": "2026-05-28"},
        {"name": "Kurban Bayramı 3. Gün", "date": "2026-05-29"},
        {"name": "Kurban Bayramı 4. Gün", "date": "2026-05-30"},
        {"name": "Demokrasi ve Milli Birlik Günü", "date": "2026-07-15"},
        {"name": "Zafer Bayramı", "date": "2026-08-30"},
        {"name": "Cumhuriyet Bayramı", "date": "2026-10-29"},
    ],
}
