from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, UserLogin, Token
from ..utils.auth import (
    get_user_by_email, get_password_hash, verify_password, 
    create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# CORS preflight handlers
@router.options("/register")
async def options_register():
    """Handle CORS preflight for register endpoint."""
    return Response(status_code=200, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age": "86400",
    })

@router.options("/login")
async def options_login():
    """Handle CORS preflight for login endpoint."""
    return Response(status_code=200, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age": "86400",
    })

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Register API called with email: {user.email}, password length: {len(user.password)}")
    
    # Check if user already exists
    if get_user_by_email(db, user.email):
        logger.warning(f"Email already registered: {user.email}")
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Validate password length (before bcrypt limit)
    if len(user.password) > 72:
        logger.error(f"Password too long: {len(user.password)} characters")
        raise HTTPException(
            status_code=400,
            detail="Password cannot be longer than 72 characters"
        )
    
    # Truncate password to 72 bytes for bcrypt compatibility
    password_to_hash = user.password[:72]
    logger.info(f"Password truncated to {len(password_to_hash)} bytes")
    
    # Create new user
    hashed_password = get_password_hash(password_to_hash)
    db_user = User(
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"User created successfully: {user.email}")
        
    # Convert User model to dict for Pydantic response
    user_dict = {
        "id": db_user.id,
        "email": db_user.email,
        "created_at": db_user.created_at
    }
    return user_dict

@router.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    # Authenticate user
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user
