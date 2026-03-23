from fastapi import APIRouter, Depends, HTTPException, Response
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
    
    # Generate next employee ID if not provided
    if not employee.employee_id:
        employee.employee_id = get_next_employee_id(db)
        
    db_employee = create_employee(db, employee)
    
    # Convert Employee model to dict for Pydantic response
    employee_dict = {
        "id": db_employee.id,
        "employee_id": db_employee.employee_id,
        "full_name": db_employee.full_name,
        "email": db_employee.email,
        "department": db_employee.department,
        "created_at": db_employee.created_at
    }
    return employee_dict

@router.get("/", response_model=List[EmployeeResponse])
def get_all_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    employees = get_employees(db)
    
    # Convert Employee models to dicts for Pydantic response
    employee_list = []
    for emp in employees:
        employee_dict = {
            "id": emp.id,
            "employee_id": emp.employee_id,
            "full_name": emp.full_name,
            "email": emp.email,
            "department": emp.department,
            "created_at": emp.created_at
        }
        employee_list.append(employee_dict)
    
    return employee_list

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
