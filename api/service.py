from fastapi import HTTPException, status
from keycloak.exceptions import KeycloakAuthenticationError
from api.config import keycloak_openid, keycloak_admin
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
            user_info = keycloak_openid.userinfo(token)
            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )

            user_id = keycloak_admin.get_user_id(username=user_info["preferred_username"])

            user_roles = keycloak_admin.get_user_roles(user_id)

            if not any(role in REQUIRED_ROLES for role in user_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User does not have required roles"
                )

            return Report(
                preferred_username=user_info["preferred_username"],
                email=user_info.get("email"),
                full_name=user_info.get("name"),
            )
        except KeycloakAuthenticationError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            ) from exc
