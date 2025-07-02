from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv

load_dotenv()

clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

def authenticate_user(request):
    """
    Authenticates a user based on the request headers using Clerk's SDK.
    Args:
        request: The incoming request object containing headers for authentication.
    Returns:
        A dictionary containing the user ID if authentication is successful.
    Raises:
        HTTPException: If authentication fails or if there is an error during the process.
    """
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173", "http://localhost:5174"], 
                jwt_key=os.getenv("JWT_KEY")
            )
        )
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        user_id = request_state.payload.get("sub")
        
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e