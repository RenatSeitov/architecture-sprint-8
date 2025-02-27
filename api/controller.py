from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.models import Report
from api.service import AuthService
from typing import List

# Initialize HTTPBearer security dependency
bearer_scheme = HTTPBearer()


class AuthController:

    @staticmethod
    def protected_endpoint(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ) ->List[Report]:
        """
        Access a protected resource that requires valid token authentication.

        Args:
            credentials (HTTPAuthorizationCredentials): Bearer token provided
            via HTTP Authorization header.

        Raises:
            HTTPException: If the token is invalid or not provided.

        Returns:
            UserInfo: Information about the authenticated user.
        """
        # Extract the bearer token from the provided credentials
        token = credentials.credentials

        # Verify the token and get user information
        user_info = AuthService.verify_token(token)

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            

        return [
                    {"id": 1, "content": "Report 1"},
                    {"id": 2, "content": "Report 2"}
                ]