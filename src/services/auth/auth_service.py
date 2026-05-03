"""
Authentication service - business logic for signup, login, and token management
"""

from typing import Optional, Dict, Tuple
from uuid import UUID
import json
import secrets
import hashlib
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
import pyotp

from models.user import User, UserRole, UserStatus
from models.tenant import Tenant, SubscriptionPlan, TenantStatus
from models.refresh_token import RefreshToken
from models.audit_log import AuditLog
from models.user_mfa import UserMFA
from schemas.auth import SignupRequest, LoginRequest
from services.auth.token_service import TokenService
from utils.password import hash_password, verify_password, validate_password_strength
from config import settings
from datetime import datetime, timedelta


class AuthService:
    """Authentication service"""

    _login_attempts: Dict[str, Dict[str, object]] = {}

    @staticmethod
    def _now() -> datetime:
        return datetime.utcnow()

    @staticmethod
    def _is_locked(email: str) -> Tuple[bool, int]:
        state = AuthService._login_attempts.get(email.lower())
        if not state:
            return False, 0
        locked_until = state.get("locked_until")
        if locked_until and locked_until > AuthService._now():
            remaining = int((locked_until - AuthService._now()).total_seconds())
            return True, max(1, remaining)
        return False, 0

    @staticmethod
    def _register_failed_attempt(email: str) -> None:
        key = email.lower()
        state = AuthService._login_attempts.setdefault(key, {"count": 0, "locked_until": None})
        state["count"] = int(state.get("count", 0)) + 1
        max_attempts = 5
        lock_minutes = 15
        if state["count"] >= max_attempts:
            state["locked_until"] = AuthService._now() + timedelta(minutes=lock_minutes)

    @staticmethod
    def _clear_failed_attempts(email: str) -> None:
        AuthService._login_attempts.pop(email.lower(), None)

    @staticmethod
    def _log_auth_event(
        db: Session,
        action: str,
        user_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict] = None,
    ) -> None:
        """Write best-effort auth audit event without interrupting main flow."""
        try:
            entry = AuditLog(
                user_id=user_id,
                tenant_id=tenant_id,
                entity_type="auth",
                entity_id=user_id,
                action=action,
                new_values=json.dumps(details or {}),
                ip_address=ip_address,
                user_agent=user_agent,
            )
            db.add(entry)
            db.commit()
        except Exception:
            db.rollback()

    @staticmethod
    def _store_refresh_token(db: Session, user_id: int, refresh_token: str) -> None:
        token_hash = TokenService.hash_token(refresh_token)
        expires_at = AuthService._now() + timedelta(days=settings.JWT_REFRESH_EXPIRATION_DAYS)
        token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            is_revoked=False,
        )
        db.add(token)
        db.commit()

    @staticmethod
    def _create_token_bundle(db: Session, user: User, tenant: Tenant, permissions: list) -> Dict:
        tokens = TokenService.create_tokens(
            user_id=user.id,
            email=user.email,
            tenant_id=tenant.id,
            tenant_code=tenant.tenant_code,
            role=user.role.value,
            permissions=permissions,
        )
        AuthService._store_refresh_token(db, user.id, tokens["refresh_token"])
        return tokens

    @staticmethod
    def _hash_backup_code(code: str) -> str:
        return hashlib.sha256(code.encode("utf-8")).hexdigest()

    @staticmethod
    def _generate_backup_codes(count: int = 8) -> list:
        return [secrets.token_hex(4).upper() for _ in range(count)]

    @staticmethod
    def _get_user_mfa(db: Session, user_id: int) -> Optional[UserMFA]:
        return db.query(UserMFA).filter(UserMFA.user_id == user_id).first()

    @staticmethod
    def generate_tenant_code(company_name: str) -> str:
        """
        Generate tenant code from company name
        
        Args:
            company_name: Company name
            
        Returns:
            Tenant code (e.g., BTM from BTM Group)
        """
        # Take first letters of each word up to 3 words
        words = company_name.split()[:3]
        code = ''.join([word[0].upper() for word in words if word])
        return code[:20]  # Max 20 chars

    @staticmethod
    def signup(
        db: Session,
        data: SignupRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[bool, Dict, Optional[str]]:
        """
        Register new user and create tenant
        
        Args:
            db: Database session
            data: Signup request data
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            # Validate password strength
            is_strong, error = validate_password_strength(data.password)
            if not is_strong:
                return False, {}, error

            # Check if email already exists globally
            existing_user = db.query(User).filter(User.email == data.email).first()
            if existing_user:
                return False, {}, "Email already registered"

            # Generate tenant code
            tenant_code = AuthService.generate_tenant_code(data.company_name)

            # Check if tenant code already exists
            existing_tenant = db.query(Tenant).filter(
                Tenant.tenant_code == tenant_code
            ).first()
            counter = 1
            while existing_tenant:
                tenant_code = f"{tenant_code}{counter}"
                existing_tenant = db.query(Tenant).filter(
                    Tenant.tenant_code == tenant_code
                ).first()
                counter += 1

            # Create tenant
            tenant = Tenant(
                tenant_code=tenant_code,
                company_name=data.company_name,
                company_email=data.email,
                phone=data.company_phone,
                city=data.company_city,
                subscription_plan=SubscriptionPlan.FREE,
                status=TenantStatus.ACTIVE
            )
            db.add(tenant)
            db.flush()  # Flush to get tenant ID without committing

            # Create user with TENANT_OWNER role
            password_hash = hash_password(data.password)
            default_permissions = [
                "create_deal",
                "view_deal",
                "edit_deal",
                "delete_deal",
                "add_payment",
                "view_payment",
                "add_client",
                "view_client",
                "edit_client",
                "add_user",
                "manage_user",
                "view_reports",
            ]

            user = User(
                tenant_id=tenant.id,
                email=data.email,
                password_hash=password_hash,
                first_name=data.first_name,
                last_name=data.last_name,
                phone=data.phone,
                role=UserRole.TENANT_OWNER,
                permissions=json.dumps(default_permissions),
                status=UserStatus.ACTIVE,
                email_verified=False
            )
            db.add(user)
            db.commit()

            # Generate tokens and persist refresh token for rotation.
            tokens = AuthService._create_token_bundle(db, user, tenant, default_permissions)

            AuthService._log_auth_event(
                db,
                action="signup_success",
                user_id=user.id,
                tenant_id=tenant.id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={"email": user.email, "role": user.role.value},
            )

            response_data = {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role.value,
                    "status": user.status.value,
                    "created_at": user.created_at.isoformat()
                },
                "tenant": {
                    "id": str(tenant.id),
                    "tenant_code": tenant.tenant_code,
                    "company_name": tenant.company_name,
                    "subscription_plan": tenant.subscription_plan.value,
                    "status": tenant.status.value
                },
                "tokens": tokens
            }

            return True, response_data, None

        except IntegrityError as e:
            db.rollback()
            return False, {}, "Email or company already exists"
        except Exception as e:
            db.rollback()
            return False, {}, str(e)

    @staticmethod
    def login(
        db: Session,
        data: LoginRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[bool, Dict, Optional[str]]:
        """
        User login
        
        Args:
            db: Database session
            data: Login request data
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            is_locked, remaining_seconds = AuthService._is_locked(data.email)
            if is_locked:
                return False, {}, f"Too many failed login attempts. Try again in {remaining_seconds} seconds"

            # Find user by email
            user = db.query(User).filter(User.email == data.email).first()
            if not user:
                AuthService._register_failed_attempt(data.email)
                AuthService._log_auth_event(
                    db,
                    action="login_failed",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={"email": data.email, "reason": "user_not_found"},
                )
                return False, {}, "Invalid email or password"

            # Verify password
            if not verify_password(data.password, user.password_hash):
                AuthService._register_failed_attempt(data.email)
                AuthService._log_auth_event(
                    db,
                    action="login_failed",
                    user_id=user.id,
                    tenant_id=user.tenant_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={"email": data.email, "reason": "invalid_password"},
                )
                return False, {}, "Invalid email or password"

            # Check if user is active
            if user.status != UserStatus.ACTIVE:
                AuthService._log_auth_event(
                    db,
                    action="login_failed",
                    user_id=user.id,
                    tenant_id=user.tenant_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={"email": data.email, "reason": f"status_{user.status.value.lower()}"},
                )
                return False, {}, f"User is {user.status.value.lower()}"

            # Get tenant info
            tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
            if not tenant:
                return False, {}, "Tenant not found"

            mfa_config = AuthService._get_user_mfa(db, user.id)
            # TODO: Enable MFA requirement for production
            # For development/testing, skip MFA requirement
            # if user.role in [UserRole.PLATFORM_ADMIN, UserRole.SUPER_ADMIN]:
            #     if not mfa_config or not mfa_config.is_enabled:
            #         AuthService._log_auth_event(
            #             db,
            #             action="login_failed",
            #             user_id=user.id,
            #             tenant_id=user.tenant_id,
            #             ip_address=ip_address,
            #             user_agent=user_agent,
            #             details={"email": data.email, "reason": "admin_mfa_not_enabled"},
            #         )
            #         return False, {}, "MFA setup is required for admin accounts"

            if mfa_config and mfa_config.is_enabled:
                mfa_token = TokenService.create_mfa_challenge_token(str(user.id))
                return True, {
                    "requires_mfa": True,
                    "mfa_token": mfa_token,
                    "user": {
                        "id": str(user.id),
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role.value,
                        "status": user.status.value,
                        "tenant_id": str(user.tenant_id),
                    },
                }, None

            # Update last login
            from datetime import datetime
            user.last_login = datetime.utcnow()
            db.commit()

            # Parse permissions
            permissions = json.loads(user.permissions) if user.permissions else []

            # Generate tokens and rotate persisted refresh token.
            tokens = AuthService._create_token_bundle(db, user, tenant, permissions)
            AuthService._clear_failed_attempts(data.email)
            AuthService._log_auth_event(
                db,
                action="login_success",
                user_id=user.id,
                tenant_id=user.tenant_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={"email": data.email},
            )

            response_data = {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role.value,
                    "status": user.status.value,
                    "tenant_id": str(user.tenant_id)
                },
                "tokens": tokens
            }

            return True, response_data, None

        except Exception as e:
            return False, {}, str(e)

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User object or None
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_tenant_by_id(db: Session, tenant_id: UUID) -> Optional[Tenant]:
        """
        Get tenant by ID
        
        Args:
            db: Database session
            tenant_id: Tenant ID
            
        Returns:
            Tenant object or None
        """
        return db.query(Tenant).filter(Tenant.id == tenant_id).first()

    @staticmethod
    def refresh_access_token(
        db: Session,
        refresh_token: str
    ) -> Tuple[bool, Dict, Optional[str]]:
        """
        Refresh access token
        
        Args:
            db: Database session
            refresh_token: Refresh token string
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            is_valid, _, payload_or_error = TokenService.refresh_access_token(refresh_token)
            if not is_valid:
                return False, {}, payload_or_error.get("error", "Invalid refresh token")

            payload = payload_or_error

            token_hash = TokenService.hash_token(refresh_token)
            stored_token = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
            if not stored_token:
                return False, {}, "Refresh token not recognized"
            if stored_token.is_revoked or stored_token.used_at is not None:
                return False, {}, "Refresh token already used or revoked"
            if stored_token.is_expired():
                return False, {}, "Refresh token expired"

            user_id = payload.get("sub")
            user = AuthService.get_user_by_id(db, user_id)
            if not user:
                return False, {}, "User not found"

            tenant = AuthService.get_tenant_by_id(db, user.tenant_id)
            if not tenant:
                return False, {}, "Tenant not found"

            permissions = json.loads(user.permissions) if user.permissions else []

            # Rotate refresh token: invalidate old and issue a new pair.
            stored_token.is_revoked = True
            stored_token.used_at = AuthService._now()
            stored_token.revoked_at = AuthService._now()
            stored_token.revoked_reason = "rotated"
            db.commit()

            tokens = AuthService._create_token_bundle(db, user, tenant, permissions)
            AuthService._log_auth_event(
                db,
                action="token_rotated",
                user_id=user.id,
                tenant_id=user.tenant_id,
                details={"reason": "refresh_used"},
            )

            response_data = {
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "token_type": "Bearer",
                "expires_in": settings.JWT_EXPIRATION_HOURS * 3600,
            }

            return True, response_data, None

        except Exception as e:
            return False, {}, str(e)

    @staticmethod
    def google_oauth_signup(
        db: Session,
        google_user_info: Dict
    ) -> Tuple[bool, Dict, Optional[str]]:
        """
        Handle Google OAuth signup (first-time user)
        
        Args:
            db: Database session
            google_user_info: User info from Google token
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            email = google_user_info.get("email")
            
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                # User exists, trigger login instead
                return False, {}, "User already exists. Please login."

            # Generate tenant code from email domain or create default
            company_name = email.split("@")[0].replace(".", " ").title()
            tenant_code = AuthService.generate_tenant_code(company_name)

            # Check if tenant code already exists
            existing_tenant = db.query(Tenant).filter(
                Tenant.tenant_code == tenant_code
            ).first()
            counter = 1
            while existing_tenant:
                tenant_code = f"{tenant_code}{counter}"
                existing_tenant = db.query(Tenant).filter(
                    Tenant.tenant_code == tenant_code
                ).first()
                counter += 1

            # Create tenant for this Google user
            tenant = Tenant(
                tenant_code=tenant_code,
                company_name=company_name,
                company_email=email,
                subscription_plan=SubscriptionPlan.FREE,
                status=TenantStatus.ACTIVE
            )
            db.add(tenant)
            db.flush()

            # Create user with TENANT_OWNER role
            default_permissions = [
                "create_deal",
                "view_deal",
                "edit_deal",
                "delete_deal",
                "add_payment",
                "view_payment",
                "add_client",
                "view_client",
                "edit_client",
                "add_user",
                "manage_user",
                "view_reports",
            ]

            user = User(
                tenant_id=tenant.id,
                email=email,
                password_hash=hash_password("oauth_" + google_user_info.get("google_id", "")),
                first_name=google_user_info.get("first_name", ""),
                last_name=google_user_info.get("last_name", ""),
                avatar_url=google_user_info.get("avatar_url"),
                role=UserRole.TENANT_OWNER,
                permissions=json.dumps(default_permissions),
                status=UserStatus.ACTIVE,
                email_verified=google_user_info.get("email_verified", False)
            )
            db.add(user)
            db.commit()

            # Generate tokens and persist refresh token for rotation.
            tokens = AuthService._create_token_bundle(db, user, tenant, default_permissions)

            response_data = {
                "is_new_user": True,
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "avatar_url": user.avatar_url,
                    "role": user.role.value,
                    "status": user.status.value,
                    "created_at": user.created_at.isoformat()
                },
                "tenant": {
                    "id": str(tenant.id),
                    "tenant_code": tenant.tenant_code,
                    "company_name": tenant.company_name,
                    "subscription_plan": tenant.subscription_plan.value,
                    "status": tenant.status.value
                },
                "tokens": tokens
            }

            return True, response_data, None

        except IntegrityError as e:
            db.rollback()
            return False, {}, "Email already exists"
        except Exception as e:
            db.rollback()
            return False, {}, str(e)

    @staticmethod
    def google_oauth_login(
        db: Session,
        google_user_info: Dict
    ) -> Tuple[bool, Dict, Optional[str]]:
        """
        Handle Google OAuth login (existing user)
        
        Args:
            db: Database session
            google_user_info: User info from Google token
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            email = google_user_info.get("email")

            # Find user by email
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return False, {}, "User not found. Please signup first."

            # Check if user is active
            if user.status != UserStatus.ACTIVE:
                return False, {}, f"User is {user.status.value.lower()}"

            # Get tenant info
            tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
            if not tenant:
                return False, {}, "Tenant not found"

            # Update last login and email verified status
            user.last_login = datetime.utcnow()
            if not user.email_verified:
                user.email_verified = google_user_info.get("email_verified", False)
            db.commit()

            # Parse permissions
            permissions = json.loads(user.permissions) if user.permissions else []

            # Generate tokens and persist refresh token for rotation.
            tokens = AuthService._create_token_bundle(db, user, tenant, permissions)

            response_data = {
                "is_new_user": False,
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "avatar_url": user.avatar_url,
                    "role": user.role.value,
                    "status": user.status.value,
                    "tenant_id": str(user.tenant_id)
                },
                "tokens": tokens
            }

            return True, response_data, None

        except Exception as e:
            return False, {}, str(e)

    @staticmethod
    def admin_signup(
        db: Session,
        data: SignupRequest
    ) -> Tuple[bool, Dict, Optional[str]]:
        """
        Admin signup - creates admin user (no tenant)
        
        Args:
            db: Database session
            data: Signup request data
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            # Validate password strength
            is_strong, error = validate_password_strength(data.password)
            if not is_strong:
                return False, {}, error

            # Check if email already exists
            existing_user = db.query(User).filter(User.email == data.email).first()
            if existing_user:
                return False, {}, "Email already registered"

            # Create admin user (no tenant - system admin)
            password_hash = hash_password(data.password)
            admin_permissions = [
                "view_all_tenants",
                "manage_tenants",
                "manage_admins",
                "view_reports",
                "manage_settings",
                "view_audit_logs",
            ]

            # For now, we need a tenant, so create a system tenant if it doesn't exist
            system_tenant = db.query(Tenant).filter(
                Tenant.tenant_code == "SYSTEM"
            ).first()
            
            if not system_tenant:
                system_tenant = Tenant(
                    tenant_code="SYSTEM",
                    company_name="System Admin",
                    subscription_plan=SubscriptionPlan.ENTERPRISE,
                    status=TenantStatus.ACTIVE
                )
                db.add(system_tenant)
                db.flush()

            user = User(
                tenant_id=system_tenant.id,
                email=data.email,
                password_hash=password_hash,
                first_name=data.first_name,
                last_name=data.last_name,
                phone=data.phone,
                role=UserRole.PLATFORM_ADMIN,
                permissions=json.dumps(admin_permissions),
                status=UserStatus.ACTIVE,
                email_verified=False
            )
            db.add(user)
            db.commit()

            # Generate tokens and persist refresh token for rotation.
            tokens = AuthService._create_token_bundle(db, user, system_tenant, admin_permissions)

            response_data = {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role.value,
                    "status": user.status.value,
                    "created_at": user.created_at.isoformat()
                },
                "tokens": tokens,
                "admin": True
            }

            return True, response_data, None

        except IntegrityError as e:
            db.rollback()
            return False, {}, "Email already exists"
        except Exception as e:
            db.rollback()
            return False, {}, str(e)

    @staticmethod
    def forgot_password(db: Session, email: str) -> Tuple[bool, Dict, Optional[str]]:
        """Issue a short-lived password reset token (dev-visible token for testing)."""
        try:
            user = db.query(User).filter(User.email == email).first()
            # Return generic success even when user does not exist to prevent account enumeration.
            if not user:
                return True, {"message": "If the email exists, a reset link has been sent"}, None

            reset_token = TokenService.create_password_reset_token(str(user.id), expires_minutes=30)
            AuthService._log_auth_event(
                db,
                action="password_reset_requested",
                user_id=user.id,
                tenant_id=user.tenant_id,
                details={"email": email},
            )

            data = {"message": "If the email exists, a reset link has been sent"}
            if settings.ENVIRONMENT.lower() != "production":
                data["reset_token"] = reset_token
            return True, data, None
        except Exception as e:
            return False, {}, str(e)

    @staticmethod
    def reset_password(
        db: Session,
        token: str,
        new_password: str,
        confirm_password: str,
    ) -> Tuple[bool, Dict, Optional[str]]:
        """Reset password and revoke existing refresh tokens."""
        try:
            if new_password != confirm_password:
                return False, {}, "Passwords do not match"

            is_strong, error = validate_password_strength(new_password)
            if not is_strong:
                return False, {}, error

            is_valid, payload, token_error = TokenService.verify_password_reset_token(token)
            if not is_valid:
                return False, {}, token_error or "Invalid reset token"

            user_id = payload.get("sub")
            user = AuthService.get_user_by_id(db, user_id)
            if not user:
                return False, {}, "User not found"

            user.password_hash = hash_password(new_password)
            db.commit()

            db.query(RefreshToken).filter(
                RefreshToken.user_id == user.id,
                RefreshToken.is_revoked == False,
            ).update(
                {
                    RefreshToken.is_revoked: True,
                    RefreshToken.revoked_reason: "password_reset",
                    RefreshToken.revoked_at: AuthService._now(),
                },
                synchronize_session=False,
            )
            db.commit()

            AuthService._log_auth_event(
                db,
                action="password_reset_completed",
                user_id=user.id,
                tenant_id=user.tenant_id,
                details={"email": user.email},
            )

            return True, {"message": "Password reset successful"}, None
        except Exception as e:
            db.rollback()
            return False, {}, str(e)

    @staticmethod
    def mfa_setup(db: Session, user_id: int) -> Tuple[bool, Dict, Optional[str]]:
        """Create or rotate TOTP secret and backup codes for user setup."""
        try:
            user = AuthService.get_user_by_id(db, user_id)
            if not user:
                return False, {}, "User not found"

            secret = pyotp.random_base32()
            backup_codes = AuthService._generate_backup_codes()
            backup_hashes = [AuthService._hash_backup_code(c) for c in backup_codes]

            mfa = AuthService._get_user_mfa(db, user.id)
            if not mfa:
                mfa = UserMFA(user_id=user.id, secret=secret, is_enabled=False)
                db.add(mfa)
            mfa.secret = secret
            mfa.is_enabled = False
            mfa.backup_codes = json.dumps(backup_hashes)
            db.commit()

            totp = pyotp.TOTP(secret)
            otpauth_url = totp.provisioning_uri(name=user.email, issuer_name=settings.PROJECT_NAME)

            return True, {
                "secret": secret,
                "otpauth_url": otpauth_url,
                "backup_codes": backup_codes,
            }, None
        except Exception as e:
            db.rollback()
            return False, {}, str(e)

    @staticmethod
    def mfa_verify_setup(db: Session, user_id: int, code: str) -> Tuple[bool, Dict, Optional[str]]:
        """Verify first TOTP code and enable MFA."""
        try:
            mfa = AuthService._get_user_mfa(db, user_id)
            if not mfa:
                return False, {}, "MFA setup not initialized"

            totp = pyotp.TOTP(mfa.secret)
            if not totp.verify(code, valid_window=1):
                return False, {}, "Invalid MFA code"

            mfa.is_enabled = True
            mfa.last_verified_at = AuthService._now()
            db.commit()

            user = AuthService.get_user_by_id(db, user_id)
            AuthService._log_auth_event(
                db,
                action="mfa_enabled",
                user_id=user_id,
                tenant_id=user.tenant_id if user else None,
            )
            return True, {"message": "MFA enabled successfully"}, None
        except Exception as e:
            db.rollback()
            return False, {}, str(e)

    @staticmethod
    def mfa_disable(db: Session, user_id: int, code: str) -> Tuple[bool, Dict, Optional[str]]:
        """Disable MFA after valid TOTP verification."""
        try:
            mfa = AuthService._get_user_mfa(db, user_id)
            if not mfa or not mfa.is_enabled:
                return False, {}, "MFA is not enabled"

            totp = pyotp.TOTP(mfa.secret)
            if not totp.verify(code, valid_window=1):
                return False, {}, "Invalid MFA code"

            mfa.is_enabled = False
            mfa.last_verified_at = AuthService._now()
            db.commit()

            user = AuthService.get_user_by_id(db, user_id)
            AuthService._log_auth_event(
                db,
                action="mfa_disabled",
                user_id=user_id,
                tenant_id=user.tenant_id if user else None,
            )
            return True, {"message": "MFA disabled successfully"}, None
        except Exception as e:
            db.rollback()
            return False, {}, str(e)

    @staticmethod
    def mfa_verify_login(
        db: Session,
        mfa_token: str,
        code: Optional[str] = None,
        backup_code: Optional[str] = None,
    ) -> Tuple[bool, Dict, Optional[str]]:
        """Complete MFA challenge and issue normal access/refresh tokens."""
        try:
            is_valid, payload, token_error = TokenService.verify_mfa_challenge_token(mfa_token)
            if not is_valid:
                return False, {}, token_error or "Invalid MFA challenge"

            user_id = payload.get("sub")
            user = AuthService.get_user_by_id(db, user_id)
            if not user:
                return False, {}, "User not found"

            if user.status != UserStatus.ACTIVE:
                return False, {}, f"User is {user.status.value.lower()}"

            tenant = AuthService.get_tenant_by_id(db, user.tenant_id)
            if not tenant:
                return False, {}, "Tenant not found"

            mfa = AuthService._get_user_mfa(db, user.id)
            if not mfa or not mfa.is_enabled:
                return False, {}, "MFA is not enabled for this user"

            verified = False
            verification_method = None
            if code:
                totp = pyotp.TOTP(mfa.secret)
                verified = totp.verify(code, valid_window=1)
                if verified:
                    verification_method = "totp"
            elif backup_code:
                backup_hashes = json.loads(mfa.backup_codes or "[]")
                provided_hash = AuthService._hash_backup_code(backup_code)
                if provided_hash in backup_hashes:
                    backup_hashes.remove(provided_hash)
                    mfa.backup_codes = json.dumps(backup_hashes)
                    verified = True
                    verification_method = "backup_code"

            if not verified:
                return False, {}, "Invalid MFA verification code"

            user.last_login = AuthService._now()
            mfa.last_verified_at = AuthService._now()
            db.commit()

            permissions = json.loads(user.permissions) if user.permissions else []
            tokens = AuthService._create_token_bundle(db, user, tenant, permissions)

            AuthService._log_auth_event(
                db,
                action="login_success_mfa",
                user_id=user.id,
                tenant_id=user.tenant_id,
                details={"email": user.email, "method": verification_method},
            )

            if verification_method == "backup_code":
                AuthService._log_auth_event(
                    db,
                    action="mfa_backup_code_used",
                    user_id=user.id,
                    tenant_id=user.tenant_id,
                    details={"email": user.email},
                )

            return True, {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role.value,
                    "status": user.status.value,
                    "tenant_id": str(user.tenant_id),
                },
                "tokens": tokens,
            }, None
        except Exception as e:
            db.rollback()
            return False, {}, str(e)
