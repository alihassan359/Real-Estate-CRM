"""
User Service - Business logic for user management
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.user import User, UserRole, UserStatus
from schemas.user import UserCreateRequest, UserUpdateRequest, UserRoleUpdateRequest
from utils.password import hash_password, verify_password
from config.permissions import get_user_permissions


class UserService:
    """Service for user management operations"""
    
    @staticmethod
    def create_user(
        db: Session,
        tenant_id: int,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: UserRole,
        phone: Optional[str] = None,
        created_by: Optional[int] = None,
    ) -> User:
        """Create a new user"""
        
        # Check if user already exists in this tenant
        existing = db.query(User).filter(
            and_(
                User.tenant_id == tenant_id,
                User.email == email
            )
        ).first()
        
        if existing:
            raise ValueError(f"User with email {email} already exists in this tenant")
        
        # Create user
        user = User(
            tenant_id=tenant_id,
            email=email,
            password_hash=hash_password(password),
            first_name=first_name,
            last_name=last_name,
            role=role,
            phone=phone,
            status=UserStatus.ACTIVE,
            created_by=created_by,
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_tenant_users(
        db: Session,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
        role: Optional[UserRole] = None,
        status: Optional[UserStatus] = None,
    ) -> tuple[List[User], int]:
        """Get all users for a tenant with pagination"""
        
        query = db.query(User).filter(User.tenant_id == tenant_id)
        
        # Apply filters
        if role:
            query = query.filter(User.role == role)
        if status:
            query = query.filter(User.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        users = query.offset(skip).limit(limit).all()
        
        return users, total
    
    @staticmethod
    def update_user_profile(
        db: Session,
        user_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> User:
        """Update user profile information"""
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if phone is not None:
            user.phone = phone
        if avatar_url is not None:
            user.avatar_url = avatar_url
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def update_user_role(
        db: Session,
        user_id: int,
        new_role: UserRole,
    ) -> User:
        """Update user role"""
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.role = new_role
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def change_password(
        db: Session,
        user_id: int,
        current_password: str,
        new_password: str,
    ) -> User:
        """Change user password"""
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise ValueError("Current password is incorrect")
        
        # Update password
        user.password_hash = hash_password(new_password)
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def reset_password(
        db: Session,
        user_id: int,
        new_password: str,
    ) -> User:
        """Reset user password (admin action)"""
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.password_hash = hash_password(new_password)
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def disable_user(
        db: Session,
        user_id: int,
        reason: Optional[str] = None,
    ) -> User:
        """Disable user (soft delete)"""
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.status = UserStatus.INACTIVE
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def enable_user(db: Session, user_id: int) -> User:
        """Enable user"""
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.status = UserStatus.ACTIVE
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def suspend_user(
        db: Session,
        user_id: int,
        reason: Optional[str] = None,
    ) -> User:
        """Suspend user account"""
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.status = UserStatus.SUSPENDED
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def record_last_login(db: Session, user_id: int) -> User:
        """Record user's last login time"""
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def verify_email(db: Session, user_id: int) -> User:
        """Mark email as verified"""
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.email_verified = True
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_permissions(user: User) -> List[str]:
        """Get all permissions for a user"""
        permissions = get_user_permissions(user.role)
        return [p.value for p in permissions]
