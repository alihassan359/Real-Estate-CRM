"""
Authentication Controller
"""

from fastapi import status
from sqlalchemy.orm import Session
from typing import Dict, Optional

from schemas.auth import (
    SignupRequest,
    LoginRequest,
    RefreshTokenRequest,
    GoogleAuthRequest,
    AdminSignupRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    MfaVerifyRequest,
    MfaDisableRequest,
    MfaLoginVerifyRequest,
)
from services.auth import AuthService
from services.auth.google_oauth_service import GoogleOAuthService


class AuthController:
    """Authentication controller"""
    
    @staticmethod
    def signup(
        db: Session,
        data: SignupRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Dict:
        """
        Handle user signup
        
        Args:
            db: Database session
            data: Signup request data
            
        Returns:
            Response dictionary
        """
        success, response_data, error = AuthService.signup(db, data, ip_address=ip_address, user_agent=user_agent)
        
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        
        return {
            "success": True,
            "message": "User registered successfully",
            "data": response_data,
            "status_code": status.HTTP_201_CREATED,
        }
    
    @staticmethod
    def login(
        db: Session,
        data: LoginRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Dict:
        """
        Handle user login
        
        Args:
            db: Database session
            data: Login request data
            
        Returns:
            Response dictionary
        """
        success, response_data, error = AuthService.login(db, data, ip_address=ip_address, user_agent=user_agent)
        
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_401_UNAUTHORIZED,
            }
        
        return {
            "success": True,
            "message": "Login successful",
            "data": response_data,
            "status_code": status.HTTP_200_OK,
        }
    
    @staticmethod
    def refresh_token(
        db: Session,
        data: RefreshTokenRequest
    ) -> Dict:
        """
        Refresh access token
        
        Args:
            db: Database session
            data: Refresh token request data
            
        Returns:
            Response dictionary
        """
        success, response_data, error = AuthService.refresh_access_token(
            db,
            data.refresh_token
        )
        
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_401_UNAUTHORIZED,
            }
        
        return {
            "success": True,
            "message": "Token refreshed successfully",
            "data": response_data,
            "status_code": status.HTTP_200_OK,
        }
    
    @staticmethod
    def logout() -> Dict:
        """
        Handle user logout
        
        Returns:
            Response dictionary
        """
        return {
            "success": True,
            "message": "Logged out successfully",
            "status_code": status.HTTP_200_OK,
        }
    
    @staticmethod
    def get_current_user(current_user: Dict) -> Dict:
        """
        Get current user info
        
        Args:
            current_user: Current user from middleware
            
        Returns:
            Response dictionary
        """
        return {
            "success": True,
            "data": current_user,
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    async def google_login(
        db: Session,
        data: GoogleAuthRequest
    ) -> Dict:
        """
        Handle Google OAuth login
        
        Args:
            db: Database session
            data: Google auth request data
            
        Returns:
            Response dictionary
        """
        try:
            # Verify Google token
            is_valid, google_user, error = await GoogleOAuthService.get_google_user_from_token(data.id_token)
            
            if not is_valid:
                return {
                    "success": False,
                    "message": error,
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                }
            
            # Try to login as existing user
            success, response_data, error = AuthService.google_oauth_login(db, google_user)
            
            if success:
                return {
                    "success": True,
                    "message": "Google login successful",
                    "data": response_data,
                    "status_code": status.HTTP_200_OK,
                }
            
            # If user not found, try signup
            success, response_data, error = AuthService.google_oauth_signup(db, google_user)
            
            if success:
                return {
                    "success": True,
                    "message": "Google signup successful",
                    "data": response_data,
                    "status_code": status.HTTP_201_CREATED,
                }
            
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }

    @staticmethod
    async def google_signup(
        db: Session,
        data: GoogleAuthRequest
    ) -> Dict:
        """
        Handle Google OAuth signup
        
        Args:
            db: Database session
            data: Google auth request data
            
        Returns:
            Response dictionary
        """
        try:
            # Verify Google token
            is_valid, google_user, error = await GoogleOAuthService.get_google_user_from_token(data.id_token)
            
            if not is_valid:
                return {
                    "success": False,
                    "message": error,
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                }
            
            # Signup new user
            success, response_data, error = AuthService.google_oauth_signup(db, google_user)
            
            if not success:
                return {
                    "success": False,
                    "message": error,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
            
            return {
                "success": True,
                "message": "Google signup successful",
                "data": response_data,
                "status_code": status.HTTP_201_CREATED,
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }

    @staticmethod
    def admin_signup(
        db: Session,
        data: AdminSignupRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Dict:
        """
        Handle admin signup
        
        Args:
            db: Database session
            data: Admin signup request data
            
        Returns:
            Response dictionary
        """
        success, response_data, error = AuthService.admin_signup(db, data)
        
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        
        return {
            "success": True,
            "message": "Admin registered successfully",
            "data": response_data,
            "status_code": status.HTTP_201_CREATED,
        }

    @staticmethod
    def admin_login(
        db: Session,
        data: LoginRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Dict:
        """
        Handle admin login
        
        Args:
            db: Database session
            data: Login request data
            
        Returns:
            Response dictionary
        """
        success, response_data, error = AuthService.login(db, data, ip_address=ip_address, user_agent=user_agent)
        
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_401_UNAUTHORIZED,
            }
        
        # Verify this is an admin user
        from models.user import UserRole
        user_role = response_data.get("user", {}).get("role")
        if user_role not in ["PLATFORM_ADMIN", "SUPER_ADMIN"]:
            return {
                "success": False,
                "message": "Access denied. Admin credentials required.",
                "status_code": status.HTTP_403_FORBIDDEN,
            }
        
        return {
            "success": True,
            "message": "Admin login successful",
            "data": response_data,
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    def forgot_password(db: Session, data: ForgotPasswordRequest) -> Dict:
        """Handle forgot password request."""
        success, response_data, error = AuthService.forgot_password(db, data.email)
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        return {
            "success": True,
            "message": response_data.get("message", "Password reset initiated"),
            "data": response_data,
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    def reset_password(db: Session, data: ResetPasswordRequest) -> Dict:
        """Handle reset password request."""
        success, response_data, error = AuthService.reset_password(
            db,
            token=data.token,
            new_password=data.new_password,
            confirm_password=data.confirm_password,
        )
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        return {
            "success": True,
            "message": response_data.get("message", "Password reset successful"),
            "data": response_data,
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    def setup_mfa(db: Session, user_id: int) -> Dict:
        """Initialize MFA setup for authenticated user."""
        success, response_data, error = AuthService.mfa_setup(db, user_id)
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        return {
            "success": True,
            "message": "MFA setup initialized",
            "data": response_data,
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    def verify_mfa_setup(db: Session, user_id: int, data: MfaVerifyRequest) -> Dict:
        """Verify MFA setup code."""
        success, response_data, error = AuthService.mfa_verify_setup(db, user_id, data.code)
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        return {
            "success": True,
            "message": response_data.get("message", "MFA enabled"),
            "data": response_data,
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    def disable_mfa(db: Session, user_id: int, data: MfaDisableRequest) -> Dict:
        """Disable MFA for authenticated user."""
        success, response_data, error = AuthService.mfa_disable(db, user_id, data.code)
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        return {
            "success": True,
            "message": response_data.get("message", "MFA disabled"),
            "data": response_data,
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    def verify_mfa_login(db: Session, data: MfaLoginVerifyRequest) -> Dict:
        """Complete MFA login challenge and issue regular tokens."""
        success, response_data, error = AuthService.mfa_verify_login(
            db,
            mfa_token=data.mfa_token,
            code=data.code,
            backup_code=data.backup_code,
        )
        if not success:
            return {
                "success": False,
                "message": error,
                "status_code": status.HTTP_401_UNAUTHORIZED,
            }
        return {
            "success": True,
            "message": "MFA login successful",
            "data": response_data,
            "status_code": status.HTTP_200_OK,
        }
