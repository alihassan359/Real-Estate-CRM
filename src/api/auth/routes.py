"""
Authentication Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from config import settings
from database.session import get_db
from schemas.auth import (
    SignupRequest,
    LoginRequest,
    RefreshTokenRequest,
    GoogleAuthRequest,
    AdminSignupRequest,
    TenantLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    MfaVerifyRequest,
    MfaDisableRequest,
    MfaLoginVerifyRequest,
)
from api.auth.controller import AuthController
from middlewares import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    data: SignupRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    User registration endpoint
    
    Creates a new tenant and user when a company signs up.
    Auto-generates tenant code and initializes with FREE plan.
    """
    result = AuthController.signup(
        db,
        data,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST),
            detail=result.get("message")
        )
    
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data")
    }


@router.post("/login")
async def login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    User login endpoint
    
    Returns JWT access and refresh tokens upon successful authentication.
    Updates last_login timestamp.
    """
    result = AuthController.login(
        db,
        data,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_401_UNAUTHORIZED),
            detail=result.get("message")
        )
    
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data")
    }


@router.post("/refresh")
async def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token endpoint
    
    Generates new access token from a valid refresh token.
    Refresh token should be sent in request body.
    """
    result = AuthController.refresh_token(db, data)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_401_UNAUTHORIZED),
            detail=result.get("message")
        )
    
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data")
    }


@router.post("/logout")
async def logout(
    current_user: dict = Depends(get_current_user)
):
    """
    User logout endpoint
    
    Requires valid JWT token.
    Token is invalidated on client side.
    """
    result = AuthController.logout()
    
    return {
        "success": result.get("success"),
        "message": result.get("message")
    }


@router.get("/me")
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """
    Get current user information
    
    Requires valid JWT token.
    Returns authenticated user details and tenant information.
    """
    result = AuthController.get_current_user(current_user)
    
    return {
        "success": result.get("success"),
        "data": result.get("data")
    }


# Health check endpoint (no auth required)
@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Public endpoint to verify API is running.
    """
    return {
        "status": "healthy",
        "service": "authentication",
        "version": "1.0.0"
    }


# ============= TENANT SIGNUP/LOGIN ENDPOINTS =============

@router.post("/tenant/signup", status_code=status.HTTP_201_CREATED)
async def tenant_signup(
    data: SignupRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Tenant signup endpoint
    
    Creates a new tenant company and owner user.
    Auto-generates tenant code and initializes with FREE plan.
    """
    result = AuthController.signup(
        db,
        data,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST),
            detail=result.get("message")
        )
    
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data")
    }


@router.post("/tenant/login")
async def tenant_login(
    data: TenantLoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Tenant login endpoint
    
    Authenticates tenant users.
    Returns JWT access and refresh tokens upon successful authentication.
    """
    # Convert to LoginRequest format
    login_data = LoginRequest(email=data.email, password=data.password)
    result = AuthController.login(
        db,
        login_data,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_401_UNAUTHORIZED),
            detail=result.get("message")
        )
    
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data")
    }


# ============= ADMIN SIGNUP/LOGIN ENDPOINTS =============

@router.post("/admin/signup", status_code=status.HTTP_201_CREATED)
async def admin_signup(
    data: AdminSignupRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Admin signup endpoint (RESTRICTED)
    
    Creates a new platform admin user.
    Admins have system-wide permissions.
    """
    result = AuthController.admin_signup(
        db,
        data,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST),
            detail=result.get("message")
        )
    
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data"),
        "admin": True
    }


@router.post("/admin/login")
async def admin_login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Admin login endpoint
    
    Authenticates platform admin users.
    Returns JWT access and refresh tokens upon successful authentication.
    """
    result = AuthController.admin_login(
        db,
        data,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_401_UNAUTHORIZED),
            detail=result.get("message")
        )
    
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data")
    }


# ============= GOOGLE OAUTH ENDPOINTS =============

@router.get("/google/auth-url")
async def get_google_auth_url():
    """
    Get Google OAuth authorization URL
    
    Frontend should redirect user to this URL for Google login.
    Include state parameter for CSRF protection.
    """
    import uuid
    state = str(uuid.uuid4())
    
    from services.auth.google_oauth_service import GoogleOAuthService
    auth_url = GoogleOAuthService.get_google_auth_url(state)
    
    return {
        "success": True,
        "auth_url": auth_url,
        "state": state
    }


@router.post("/google/login", status_code=status.HTTP_200_OK)
async def google_login(
    data: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Google OAuth login endpoint
    
    Exchange Google ID token for application tokens.
    Auto-creates tenant and user for first-time Google signup.
    """
    result = await AuthController.google_login(db, data)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_401_UNAUTHORIZED),
            detail=result.get("message")
        )
    
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "is_new_user": result.get("data", {}).get("is_new_user", False),
        "data": result.get("data")
    }


@router.post("/google/signup", status_code=status.HTTP_201_CREATED)
async def google_signup(
    data: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Google OAuth signup endpoint
    
    Exchange Google ID token for application tokens.
    Creates new tenant and user for first-time Google signup.
    """
    result = await AuthController.google_signup(db, data)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST),
            detail=result.get("message")
        )
    
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "is_new_user": True,
        "data": result.get("data")
    }


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """Generate password reset token (dev mode returns token in response)."""
    result = AuthController.forgot_password(db, data)
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST),
            detail=result.get("message")
        )
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data"),
    }


@router.post("/reset-password")
async def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Reset password using a valid password reset token."""
    result = AuthController.reset_password(db, data)
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST),
            detail=result.get("message")
        )
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data"),
    }


@router.post("/mfa/setup")
async def mfa_setup(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Initialize MFA setup and return secret, otpauth URL, and backup codes."""
    result = AuthController.setup_mfa(db, int(current_user.get("user_id")))
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST),
            detail=result.get("message"),
        )
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data"),
    }


@router.post("/mfa/verify-setup")
async def mfa_verify_setup(
    data: MfaVerifyRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Verify MFA setup by validating a TOTP code."""
    result = AuthController.verify_mfa_setup(db, int(current_user.get("user_id")), data)
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST),
            detail=result.get("message"),
        )
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data"),
    }


@router.post("/mfa/disable")
async def mfa_disable(
    data: MfaDisableRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Disable MFA for current user after code verification."""
    result = AuthController.disable_mfa(db, int(current_user.get("user_id")), data)
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST),
            detail=result.get("message"),
        )
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data"),
    }


@router.post("/mfa/verify-login")
async def mfa_verify_login(
    data: MfaLoginVerifyRequest,
    db: Session = Depends(get_db),
):
    """Complete login after MFA challenge and issue access tokens."""
    result = AuthController.verify_mfa_login(db, data)
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", status.HTTP_401_UNAUTHORIZED),
            detail=result.get("message"),
        )
    return {
        "success": result.get("success"),
        "message": result.get("message"),
        "data": result.get("data"),
    }
