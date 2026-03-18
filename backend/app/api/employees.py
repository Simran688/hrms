from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import (
    create_employee, get_employees, get_employee_by_id, 
    get_employee_by_email, delete_employee, get_next_employee_id
)
from ..schemas import EmployeeCreate, EmployeeResponse
from ..utils.auth import get_current_active_user
from ..models.user import User

router = APIRouter(prefix="/api/employees", tags=["employees"])

@router.post("/", response_model=EmployeeResponse, status_code=201)
def create_new_employee(
    employee: EmployeeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validate unique email
    if get_employee_by_email(db, employee.email):
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    # Validate unique employee_id
    if get_employee_by_id(db, employee.employee_id):
        raise HTTPException(
            status_code=400, 
            detail="Employee ID already exists"
        )
    
    return create_employee(db, employee)

@router.get("/", response_model=List[EmployeeResponse])
def get_all_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return get_employees(db)

@router.delete("/{employee_id}", status_code=204)
def delete_employee_by_id(
    employee_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not delete_employee(db, employee_id):
        raise HTTPException(
            status_code=404, 
            detail="Employee not found"
        )

@router.get("/next-id", response_model=dict)
def get_next_emp_id(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return {"next_employee_id": get_next_employee_id(db)}
