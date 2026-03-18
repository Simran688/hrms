# HRMS Lite Backend

A lightweight FastAPI backend for the Human Resource Management System.

## Features

- Employee management (CRUD operations)
- Attendance tracking and reporting
- RESTful API with proper validation
- SQLite database (easily upgradeable to PostgreSQL)
- Comprehensive error handling

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (development), PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Employees
- `GET /api/employees` - Get all employees
- `POST /api/employees` - Create new employee
- `DELETE /api/employees/{employee_id}` - Delete employee
- `GET /api/employees/next-id` - Get next employee ID

### Attendance
- `POST /api/attendance` - Mark attendance
- `GET /api/attendance/{employee_id}` - Get attendance records
- `GET /api/attendance/{employee_id}/stats` - Get attendance statistics

## Database Schema

### Employees Table
- `id` (Primary Key)
- `employee_id` (Unique)
- `full_name`
- `email` (Unique)
- `department`
- `created_at`

### Attendance Table
- `id` (Primary Key)
- `employee_id` (Foreign Key)
- `date`
- `status` ('present' or 'absent')
- `created_at`

## Deployment

### Render (Recommended)
1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy automatically on push

### Railway
1. Connect your GitHub repository
2. Configure environment variables
3. Deploy

## Environment Variables

- `DATABASE_URL`: Database connection string
- `ALLOWED_ORIGINS`: CORS allowed origins (comma-separated)

## Development

The database will be automatically created when you first run the application.
