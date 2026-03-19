from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from .database import engine, Base
from .api import employees, attendance, auth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

app = FastAPI(
    title="HRMS Lite API",
    description="A lightweight Human Resource Management System API",
    version="1.0.0"
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
origins = [origin.strip() for origin in allowed_origins if origin.strip()]
logger.info(f"CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
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
