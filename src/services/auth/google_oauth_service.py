"""
Google OAuth Service - Handle Google authentication
"""

from typing import Optional, Dict, Tuple
from google.auth.transport import requests
from google.oauth2 import id_token
import httpx
from config import settings


class GoogleOAuthService:
    """Google OAuth service"""

    @staticmethod
    async def get_google_user_from_token(token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Verify Google token and get user info
        
        Args:
            token: Google ID token
            
        Returns:
            Tuple of (success, user_info, error)
        """
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            # Token is valid, extract user info
            user_info = {
                "email": idinfo.get("email"),
                "first_name": idinfo.get("given_name", ""),
                "last_name": idinfo.get("family_name", ""),
                "avatar_url": idinfo.get("picture"),
                "google_id": idinfo.get("sub"),
                "email_verified": idinfo.get("email_verified", False)
            }

            return True, user_info, None

        except ValueError as e:
            return False, None, f"Invalid token: {str(e)}"
        except Exception as e:
            return False, None, f"OAuth error: {str(e)}"

    @staticmethod
    async def exchange_code_for_token(code: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from Google
            
        Returns:
            Tuple of (success, id_token, error)
        """
        try:
            token_url = "https://oauth2.googleapis.com/token"
            
            payload = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.GOOGLE_REDIRECT_URI
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=payload)
                
                if response.status_code != 200:
                    return False, None, "Failed to exchange code for token"

                data = response.json()
                id_token_value = data.get("id_token")

                if not id_token_value:
                    return False, None, "No ID token in response"

                return True, id_token_value, None

        except Exception as e:
            return False, None, f"Token exchange error: {str(e)}"

    @staticmethod
    def get_google_auth_url(state: str) -> str:
        """
        Get Google OAuth authorization URL
        
        Args:
            state: State for CSRF protection
            
        Returns:
            Google OAuth URL
        """
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state
        }

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
