"""
Standard API Response Utilities
"""

from typing import Any, Optional, Dict
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """Standard API response model"""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[Dict] = None


def success_response(message: str, data: Any = None) -> Dict:
    """Create success response"""
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message: str, error: Dict = None) -> Dict:
    """Create error response"""
    return {
        "success": False,
        "message": message,
        "error": error or {},
    }
