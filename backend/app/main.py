from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from .database import engine, Base
from .api import employees, attendance, auth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Force create database tables with detailed logging
try:
    logger.info("Starting database table creation...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"Tables in database: {tables}")
    
except Exception as e:
    logger.error(f"Error creating database tables: {e}")
    logger.error(f"Database URL: {os.getenv('DATABASE_URL', 'Not set')}")

app = FastAPI(
    title="HRMS Lite API",
    description="A lightweight Human Resource Management System API",
    version="1.0.0"
)

# 🔧 GUARANTEED CORS FIX - Allow all origins temporarily to debug
# TODO: Change back to specific origins after debugging
allowed_origins = ["*"]  # Allow all origins
origins = allowed_origins
logger.info(f"CORS DEBUG: ALLOWED_ORIGINS env var: {os.getenv('ALLOWED_ORIGINS')}")
logger.info(f"CORS DEBUG: Using origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

logger.info(f"CORS middleware configured with methods: {['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']}")
logger.info(f"CORS middleware configured with origins: {origins}")

# 🔧 OPTIONAL: Global OPTIONS handler for stubborn CORS issues
@app.options("/{full_path:path}")
async def handle_options(request: Request, full_path: str):
    """Global OPTIONS handler for CORS preflight requests."""
    logger.info(f"Global OPTIONS handler: {request.method} {full_path}")
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "86400",
        }
    )

# Include routers AFTER CORS middleware
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(attendance.router)
logger.info("Routers registered successfully")

@app.get("/")
def read_root():
    return {"message": "HRMS Lite API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/cors-test")
def cors_test():
    """Test endpoint for CORS verification."""
    return {
        "message": "CORS is working",
        "methods": "GET, POST, PUT, DELETE, OPTIONS",
        "headers": "Content-Type, Authorization"
    }
