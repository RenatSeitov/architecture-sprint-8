from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.models import Report
from api.controller import AuthController
from api.config import get_openid

# Initialize the FastAPI app
app = FastAPI()

# Initialize the HTTPBearer scheme for authentication
bearer_scheme = HTTPBearer()

# Configure client
keycloak_openid = get_openid()

# Define the root endpoint
@app.get("/reports", response_model=list[Report])
async def protected_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """
    Protected endpoint that requires a valid token for access.

    Args:
        credentials (HTTPAuthorizationCredentials):
        Bearer token provided via HTTP Authorization header.

    Returns:
        UserInfo: Information about the authenticated user.
    """
    return AuthController.protected_endpoint(credentials)