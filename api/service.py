from fastapi import HTTPException, status
from keycloak.exceptions import KeycloakAuthenticationError
from api.config import keycloak_openid
from api.models import Report

REQUIRED_ROLES = ["prothetic_user"]

class AuthService:

    @staticmethod
    def verify_token(token: str) -> Report:
        """
        Получает заголовок Authorization (Bearer <токен>),
        валидирует токен через Keycloak OpenID Introspect
        и возвращает Report-модель с данными пользователя.
        Если нужно - проверяем наличие роли(ей).
        """
        try:
            
            user_info = keycloak_openid.introspect(token)
            print("user_info from introspect:", user_info)

            if not user_info.get("active"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                )

            roles = user_info.get("realm_access", {}).get("roles", [])
            for role in REQUIRED_ROLES:
                if role not in roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Missing required role: {role}",
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
