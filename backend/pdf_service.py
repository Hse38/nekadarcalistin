"""

PDF Generation Service
Generates professional PDF reports for HR analysis.
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.pdfgen import canvas
from datetime import datetime
from typing import Dict
import os


def generate_analysis_pdf(
    employee_name: str,
    employee_surname: str,
    year: int,
    daily_working_hours: float,
    weekly_working_days: float,
    annual_leave_total: float,
    annual_leave_used: float,
    extra_leave_days: float,
    calculated_results: Dict,
    output_path: str
) -> str:
    """
    Generate a comprehensive PDF report for employee working time analysis.
    
    Args:
        employee_name: Employee first name
        employee_surname: Employee surname
        year: Analysis year
        daily_working_hours: Daily working hours
        weekly_working_days: Weekly working days
        annual_leave_total: Total annual leave entitlement
        annual_leave_used: Annual leave days used
        extra_leave_days: Extra leave days
        calculated_results: Results from calculation_service
        output_path: Path where PDF will be saved
        
    Returns:
        Path to generated PDF file
    """
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph(f"Çalışma Saati Analiz Raporu", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.5*cm))
    
    # Employee Information
    elements.append(Paragraph("Personel Bilgileri", heading_style))
    
    emp_data = [
        ['Personel Adı Soyadı:', f"{employee_name} {employee_surname}"],
        ['Analiz Yılı:', str(year)],
        ['Rapor Tarihi:', datetime.now().strftime('%d.%m.%Y %H:%M')]
    ]
    
    emp_table = Table(emp_data, colWidths=[6*cm, 10*cm])
    emp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(emp_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Working Rules
    elements.append(Paragraph("Çalışma Kuralları", heading_style))
    
    rules_data = [
        ['Günlük Çalışma Saati:', f"{daily_working_hours} saat"],
        ['Haftalık Çalışma Günü:', f"{weekly_working_days} gün"],
    ]
    
    rules_table = Table(rules_data, colWidths=[6*cm, 10*cm])
    rules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(rules_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Leave Information
    elements.append(Paragraph("İzin Bilgileri", heading_style))
    
    leave_data = [
        ['Yıllık İzin Hakkı:', f"{annual_leave_total} gün"],
        ['Kullanılan Yıllık İzin:', f"{annual_leave_used} gün"],
        ['Mazeret İzni:', f"{extra_leave_days} gün"],
    ]
    
    leave_table = Table(leave_data, colWidths=[6*cm, 10*cm])
    leave_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(leave_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Key Performance Indicators
    elements.append(Paragraph("Analiz Sonuçları", heading_style))
    
    metadata = calculated_results.get('metadata', {})
    difference = calculated_results['difference_hours']
    
    # Determine if overtime or missing
    if difference > 0:
        diff_text = f"+{difference:.2f} saat (Fazla Mesai)"
        diff_color = colors.HexColor('#10b981')
    elif difference < 0:
        diff_text = f"{difference:.2f} saat (Eksik)"
        diff_color = colors.HexColor('#ef4444')
    else:
        diff_text = "0.00 saat (Tam)"
        diff_color = colors.black
    
    kpi_data = [
        ['Metrik', 'Değer'],
        ['Teorik Çalışma Günü', f"{calculated_results['theoretical_working_days']:.2f} gün"],
        ['Fiili Çalışma Günü', f"{calculated_results['actual_working_days']} gün"],
        ['Teorik Çalışma Saati', f"{calculated_results['theoretical_working_hours']:.2f} saat"],
        ['Fiili Çalışma Saati', f"{calculated_results['actual_working_hours']:.2f} saat"],
        ['Fark', diff_text],
    ]
    
    kpi_table = Table(kpi_data, colWidths=[8*cm, 8*cm])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
    ]))
    
    elements.append(kpi_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Additional Metrics
    elements.append(Paragraph("Detaylı İstatistikler", heading_style))
    
    stats_data = [
        ['Toplam Olası Çalışma Günü:', f"{metadata.get('possible_working_days', 0):.2f} gün"],
        ['Toplam Resmi Tatil:', f"{metadata.get('total_holidays', 0)} gün"],
        ['Çalışılan Resmi Tatil:', f"{metadata.get('holidays_worked', 0)} gün"],
        ['Çalışılmayan Resmi Tatil:', f"{metadata.get('holidays_not_worked', 0)} gün"],
    ]
    
    stats_table = Table(stats_data, colWidths=[8*cm, 8*cm])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 1*cm))
    
    # Footer note
    footer_text = """
    <para align="center">
    <font size="8" color="#6b7280">
    Bu rapor HR Çalışma Saati Analiz Sistemi tarafından otomatik olarak oluşturulmuştur.<br/>
    Rapor tarihi: {date}<br/>
    </font>
    </para>
    """.format(date=datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
    
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    return output_path


def generate_filename(employee_name: str, employee_surname: str, year: int) -> str:
    """
    Generate a standardized filename for the PDF report.
    
    Args:
        employee_name: Employee first name
        employee_surname: Employee surname
        year: Analysis year
        
    Returns:
        Filename string
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = f"{employee_name}_{employee_surname}".replace(' ', '_')
    return f"HR_Analiz_{safe_name}_{year}_{timestamp}.pdf"


def generate_analysis_pdf(analysis, employee) -> bytes:
    """
    Generate PDF report for an analysis and return as bytes.
    
    Args:
        analysis: Analysis model instance
        employee: Employee model instance
        
    Returns:
        PDF content as bytes
    """
    from io import BytesIO
    
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Çalışma Saati Analiz Raporu", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.5*cm))
    
    # Employee Information
    elements.append(Paragraph("Personel Bilgileri", heading_style))
    
    emp_data = [
        ['Personel Adı Soyadı:', f"{employee.name} {employee.surname}"],
        ['Analiz Yılı:', str(analysis.year)],
        ['Rapor Tarihi:', datetime.now().strftime('%d.%m.%Y %H:%M')]
    ]
    
    emp_table = Table(emp_data, colWidths=[6*cm, 10*cm])
    emp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(emp_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Working Rules
    elements.append(Paragraph("Çalışma Kuralları", heading_style))
    
    rules_data = [
        ['Günlük Çalışma Saati:', f"{analysis.daily_working_hours} saat"],
        ['Haftalık Çalışma Günü:', f"{analysis.weekly_working_days} gün"],
    ]
    
    rules_table = Table(rules_data, colWidths=[6*cm, 10*cm])
    rules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    elements.append(rules_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Leave Information
    elements.append(Paragraph("İzin Bilgileri", heading_style))
    
    leave_data = [
        ['Yıllık İzin Hakkı:', f"{analysis.annual_leave_total} gün"],
        ['Kullanılan Yıllık İzin:', f"{analysis.annual_leave_used} gün"],
        ['Mazeret İzni:', f"{analysis.extra_leave_days} gün"],
    ]
    
    leave_table = Table(leave_data, colWidths=[6*cm, 10*cm])
    leave_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    elements.append(leave_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Key Performance Indicators
    elements.append(Paragraph("Analiz Sonuçları", heading_style))
    
    difference = analysis.difference_hours or 0
    
    if difference > 0:
        diff_text = f"+{difference:.2f} saat (Fazla Mesai)"
    elif difference < 0:
        diff_text = f"{difference:.2f} saat (Eksik)"
    else:
        diff_text = "0.00 saat (Tam)"
    
    theo_days = analysis.theoretical_working_days or 0
    actual_days = analysis.actual_working_days or 0
    theo_hours = analysis.theoretical_working_hours or 0
    actual_hours = analysis.actual_working_hours or 0
    
    kpi_data = [
        ['Metrik', 'Değer'],
        ['Teorik Çalışma Günü', f"{theo_days:.2f} gün"],
        ['Fiili Çalışma Günü', f"{actual_days} gün" if actual_days else "Veri Yok"],
        ['Teorik Çalışma Saati', f"{theo_hours:.2f} saat"],
        ['Fiili Çalışma Saati', f"{actual_hours:.2f} saat" if actual_hours else "Veri Yok"],
        ['Fark', diff_text if analysis.actual_working_hours else "-"],
    ]
    
    kpi_table = Table(kpi_data, colWidths=[8*cm, 8*cm])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
    ]))
    
    elements.append(kpi_table)
    elements.append(Spacer(1, 1*cm))
    
    # Footer
    footer_text = f"""
    <para align="center">
    <font size="8" color="#6b7280">
    Bu rapor HR Çalışma Saati Analiz Sistemi tarafından otomatik olarak oluşturulmuştur.<br/>
    Rapor tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}<br/>
    </font>
    </para>
    """
    
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    
    return buffer.getvalue()
