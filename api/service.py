from fastapi import HTTPException, status
from keycloak.exceptions import KeycloakAuthenticationError
from api.config import keycloak_openid
from api.models import Report

REQUIRED_ROLES=[
    "prothetic_user"
]

class AuthService:

    @staticmethod
    def verify_token(token: str) -> Report:
        """
        Verify the given token and return user information.
        Optionally, check if user has required roles.
        """
        try:
            user_info = keycloak_openid.introspect(f"Bearer {token}")
            print(user_info)
            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )

            return Report(
                preferred_username=user_info["preferred_username"],
                email=user_info.get("email"),
                full_name=user_info.get("name"),
            )
            return user_info
        except KeycloakAuthenticationError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            ) from exc
