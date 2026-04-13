"""
Authentication middleware for JWT token verification
"""

from typing import Optional, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from starlette.authentication import AuthCredentials
import json

from services.auth.token_service import TokenService

# HTTP Bearer for FastAPI
security = HTTPBearer()

# Define HTTPAuthCredentials if not available
try:
    from fastapi.security import HTTPAuthCredentials
except ImportError:
    from starlette.requests import Request
    
    class HTTPAuthCredentials:
        def __init__(self, scheme: str, credentials: str):
            self.scheme = scheme
            self.credentials = credentials


class AuthMiddleware:
    """Authentication middleware class"""

    @staticmethod
    def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> Dict:
        """
        Verify JWT token from Authorization header
        
        Args:
            credentials: HTTP Bearer credentials
            
        Returns:
            Decoded token payload
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        token = credentials.credentials
        
        is_valid, payload = TokenService.verify_token(token)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=payload.get("error", "Invalid token"),
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload

    @staticmethod
    def get_current_user(token_payload: Dict = Depends(verify_token)) -> Dict:
        """
        Get current user from token payload
        
        Args:
            token_payload: Decoded token payload
            
        Returns:
            User info from token
            
        Raises:
            HTTPException: If user info is missing
        """
        user_id = token_payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
            )
        
        return {
            "user_id": user_id,
            "email": token_payload.get("user_email"),
            "tenant_id": token_payload.get("tenant_id"),
            "tenant_code": token_payload.get("tenant_code"),
            "role": token_payload.get("role"),
            "permissions": token_payload.get("permissions", []),
        }

    @staticmethod
    def require_role(*allowed_roles: str):
        """
        Dependency to require specific roles
        
        Args:
            *allowed_roles: Allowed role values
            
        Returns:
            Dependency function
        """
        async def check_role(current_user: Dict = Depends(AuthMiddleware.get_current_user)):
            if current_user["role"] not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions for this operation",
                )
            return current_user
        
        return check_role

    @staticmethod
    def require_permission(permission: str):
        """
        Dependency to require specific permission
        
        Args:
            permission: Required permission
            
        Returns:
            Dependency function
        """
        async def check_permission(current_user: Dict = Depends(AuthMiddleware.get_current_user)):
            if permission not in current_user.get("permissions", []):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing permission: {permission}",
                )
            return current_user
        
        return check_permission


# Convenience dependency functions
async def get_current_user(
    token_payload: Dict = Depends(AuthMiddleware.verify_token)
) -> Dict:
    """Get current user from token"""
    return AuthMiddleware.get_current_user(token_payload)


def get_current_tenant_owner():
    """Get current user and require TENANT_OWNER role"""
    return AuthMiddleware.require_role("TENANT_OWNER")


def get_current_manager():
    """Get current user and require MANAGER role"""
    return AuthMiddleware.require_role("MANAGER", "TENANT_OWNER")
