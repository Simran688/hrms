from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import date
from .models import Employee, Attendance
from .schemas import EmployeeCreate, AttendanceCreate
from typing import List, Optional

def get_next_employee_id(db: Session) -> str:
    try:
        last_employee = db.query(Employee).order_by(Employee.id.desc()).first()
        if last_employee:
            last_num = int(last_employee.employee_id.replace("EMP", ""))
            return f"EMP{last_num + 1:04d}"
        return "EMP0001"
    except SQLAlchemyError:
        db.rollback()
        raise

def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
    try:
        db_employee = Employee(**employee.dict())
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise

def get_employees(db: Session) -> List[Employee]:
    try:
        return db.query(Employee).all()
    except SQLAlchemyError:
        db.rollback()
        raise

def get_employee_by_id(db: Session, employee_id: str) -> Optional[Employee]:
    try:
        return db.query(Employee).filter(Employee.employee_id == employee_id).first()
    except SQLAlchemyError:
        db.rollback()
        raise

def get_employee_by_email(db: Session, email: str) -> Optional[Employee]:
    try:
        return db.query(Employee).filter(Employee.email == email).first()
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_employee(db: Session, employee_id: str) -> bool:
    try:
        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if employee:
            db.delete(employee)
            db.commit()
            return True
        return False
    except SQLAlchemyError:
        db.rollback()
        raise

def create_attendance(db: Session, attendance: AttendanceCreate) -> Attendance:
    try:
        db_attendance = Attendance(**attendance.dict())
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise

def get_attendance_by_employee(db: Session, employee_id: str) -> List[Attendance]:
    try:
        return db.query(Attendance).filter(Attendance.employee_id == employee_id).all()
    except SQLAlchemyError:
        db.rollback()
        raise

def get_attendance_by_employee_and_date(db: Session, employee_id: str, date: date) -> Optional[Attendance]:
    try:
        return db.query(Attendance).filter(
            and_(Attendance.employee_id == employee_id, Attendance.date == date)
        ).first()
    except SQLAlchemyError:
        db.rollback()
        raise

def get_attendance_stats(db: Session, employee_id: str) -> dict:
    try:
        total_days = db.query(Attendance).filter(Attendance.employee_id == employee_id).count()
        present_days = db.query(Attendance).filter(
            and_(Attendance.employee_id == employee_id, Attendance.status == "present")
        ).count()
        absent_days = total_days - present_days
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        return {
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "attendance_percentage": round(attendance_percentage, 2)
        }
    except SQLAlchemyError:
        db.rollback()
        raise
