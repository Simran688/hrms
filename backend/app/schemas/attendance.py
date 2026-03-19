from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class AttendanceBase(BaseModel):
    employee_id: str
    date: date
    status: str  # 'present' or 'absent'

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AttendanceStats(BaseModel):
    total_days: int
    present_days: int
    absent_days: int
    attendance_percentage: float
