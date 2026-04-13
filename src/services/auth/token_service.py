"""
JWT Token service for generating, validating, and refreshing tokens
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from uuid import UUID, uuid4
import hashlib
import jwt
from config import settings


class TokenService:
    """JWT Token service"""

    @staticmethod
    def hash_token(token: str) -> str:
        """Return a deterministic hash for storing opaque tokens safely."""
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def create_tokens(
        user_id: UUID,
        email: str,
        tenant_id: UUID,
        tenant_code: str,
        role: str,
        permissions: list = None
    ) -> Dict[str, str]:
        """
        Create access and refresh tokens
        
        Args:
            user_id: User ID
            email: User email
            tenant_id: Tenant ID
            tenant_code: Tenant code
            role: User role
            permissions: User permissions list
            
        Returns:
            Dictionary with access_token and refresh_token
        """
        if permissions is None:
            permissions = []
        
        # Create access token
        access_token = TokenService.create_access_token(
            user_id=user_id,
            email=email,
            tenant_id=tenant_id,
            tenant_code=tenant_code,
            role=role,
            permissions=permissions
        )
        
        # Create refresh token
        refresh_token = TokenService.create_refresh_token(user_id=user_id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": settings.JWT_EXPIRATION_HOURS * 3600
        }

    @staticmethod
    def create_access_token(
        user_id: UUID,
        email: str,
        tenant_id: UUID,
        tenant_code: str,
        role: str,
        permissions: list = None,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token
        
        Args:
            user_id: User ID
            email: User email
            tenant_id: Tenant ID
            tenant_code: Tenant code
            role: User role
            permissions: User permissions
            expires_delta: Custom expiration delta
            
        Returns:
            JWT token string
        """
        if permissions is None:
            permissions = []
        
        if expires_delta is None:
            expires_delta = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "sub": str(user_id),
            "user_email": email,
            "tenant_id": str(tenant_id),
            "tenant_code": tenant_code,
            "role": role,
            "permissions": permissions,
            "iat": datetime.utcnow(),
            "exp": expire
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token

    @staticmethod
    def create_refresh_token(
        user_id: UUID,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT refresh token
        
        Args:
            user_id: User ID
            expires_delta: Custom expiration delta
            
        Returns:
            JWT refresh token string
        """
        if expires_delta is None:
            expires_delta = timedelta(days=settings.JWT_REFRESH_EXPIRATION_DAYS)
        
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "iat": datetime.utcnow(),
            "exp": expire
        }
        payload["jti"] = str(uuid4())
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token

    @staticmethod
    def verify_token(token: str) -> Tuple[bool, Optional[Dict]]:
        """
        Verify JWT token and return payload
        
        Args:
            token: JWT token string
            
        Returns:
            Tuple of (is_valid, payload)
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, {"error": "Token expired"}
        except jwt.InvalidTokenError:
            return False, {"error": "Invalid token"}

    @staticmethod
    def refresh_access_token(refresh_token: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Create new access token from refresh token
        
        Args:
            refresh_token: Refresh token string
            
        Returns:
            Tuple of (is_valid, new_access_token, error_info)
        """
        is_valid, payload = TokenService.verify_token(refresh_token)
        
        if not is_valid:
            return False, None, payload
        
        # Check if it's a refresh token
        if payload.get("type") != "refresh":
            return False, None, {"error": "Invalid token type"}
        
        # For refresh token, we would need to get user details from database
        # This will be handled in the auth service
        return True, None, payload

    @staticmethod
    def decode_token(token: str) -> Optional[Dict]:
        """
        Decode token without verification (use with caution)
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded payload or None
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_signature": True}
            )
            return payload
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def create_password_reset_token(
        user_id: str,
        expires_minutes: int = 30
    ) -> str:
        """Create a short-lived password reset token."""
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
        payload = {
            "sub": str(user_id),
            "type": "password_reset",
            "iat": datetime.utcnow(),
            "exp": expire,
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def verify_password_reset_token(token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Validate a password reset token and return payload."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            if payload.get("type") != "password_reset":
                return False, None, "Invalid token type"
            return True, payload, None
        except jwt.ExpiredSignatureError:
            return False, None, "Password reset token expired"
        except jwt.InvalidTokenError:
            return False, None, "Invalid password reset token"

    @staticmethod
    def create_mfa_challenge_token(user_id: str, expires_minutes: int = 5) -> str:
        """Create a short-lived token used to complete MFA login challenge."""
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
        payload = {
            "sub": str(user_id),
            "type": "mfa_challenge",
            "iat": datetime.utcnow(),
            "exp": expire,
            "jti": str(uuid4()),
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def verify_mfa_challenge_token(token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Validate mfa challenge token and return payload."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            if payload.get("type") != "mfa_challenge":
                return False, None, "Invalid token type"
            return True, payload, None
        except jwt.ExpiredSignatureError:
            return False, None, "MFA challenge expired"
        except jwt.InvalidTokenError:
            return False, None, "Invalid MFA challenge token"
