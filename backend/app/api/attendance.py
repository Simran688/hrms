from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from ..database import get_db
from ..crud import (
    create_attendance, get_attendance_by_employee, 
    get_attendance_by_employee_and_date, get_attendance_stats,
    get_employee_by_id
)
from ..schemas import AttendanceCreate, AttendanceResponse, AttendanceStats
from ..utils.auth import get_current_active_user
from ..models.user import User

router = APIRouter(prefix="/api/attendance", tags=["attendance"])

@router.post("/", response_model=AttendanceResponse, status_code=201)
def mark_attendance(
    attendance: AttendanceCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validate employee exists
    if not get_employee_by_id(db, attendance.employee_id):
        raise HTTPException(
            status_code=404, 
            detail="Employee not found"
        )
    
    # Check if attendance already marked for this date
    existing = get_attendance_by_employee_and_date(db, attendance.employee_id, attendance.date)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Attendance already marked for this date"
        )
    
    # Validate status
    if attendance.status not in ["present", "absent"]:
        raise HTTPException(
            status_code=400, 
            detail="Status must be 'present' or 'absent'"
        )
    
    return create_attendance(db, attendance)

@router.get("/{employee_id}", response_model=List[AttendanceResponse])
def get_employee_attendance(
    employee_id: str, 
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validate employee exists
    if not get_employee_by_id(db, employee_id):
        raise HTTPException(
            status_code=404, 
            detail="Employee not found"
        )
    
    attendance = get_attendance_by_employee(db, employee_id)
    
    # Convert Attendance models to dicts for Pydantic response
    attendance_list = []
    for record in attendance:
        attendance_dict = {
            "id": record.id,
            "employee_id": record.employee_id,
            "date": record.date,
            "status": record.status,
            "created_at": record.created_at
        }
        attendance_list.append(attendance_dict)
    
    # Filter by date range if provided
    if start_date or end_date:
        filtered_attendance = []
        for record in attendance_list:
            if start_date and record.date < start_date:
                continue
            if end_date and record.date > end_date:
                continue
            filtered_attendance.append(record)
        return filtered_attendance
    
    return attendance_list

@router.get("/{employee_id}/stats", response_model=AttendanceStats)
def get_employee_attendance_stats(
    employee_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validate employee exists
    if not get_employee_by_id(db, employee_id):
        raise HTTPException(
            status_code=404, 
            detail="Employee not found"
        )
    
    stats = get_attendance_stats(db, employee_id)
    return AttendanceStats(**stats)
