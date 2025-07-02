from logging import raiseExceptions

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.db import (
    get_challenge_quota,
    create_challenge,
    create_challenge_quota,
    reset_quota_if_needed, 
    get_user_challenges
)
from ..utils import authenticate_user
from ..database.models import get_db
import json
from datetime import datetime

router = APIRouter()

class ChallengeRequest(BaseModel):
    difficulty: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "difficulty": "easy"
            }
        }
        

@router.post("/generate-challenge")
async def generate_challenge(request: ChallengeRequest, 
                              db: Session = Depends(get_db)):
    """
    Generates a new challenge based on the specified difficulty.
    
    Args:
        request (ChallengeRequest): The request containing the challenge difficulty.
        db (Session): The database session.
        
    Returns:
        dict: A dictionary containing the generated challenge details.
    """
    try:
        user_details = authenticate_user(request)
        user_id = user_details.get("user_id")
    
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        quota = get_challenge_quota(db, user_id)
        
        if not quota:
            quota = create_challenge_quota(db, user_id)
    
        quota = reset_quota_if_needed(db, quota)
    
        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Challenge quota exceeded")
        
        challenge_data = None
        
        # TODO: Implement the logic to generate a challenge based on the difficulty
    
        # Decrement the user's challenge quota
        quota.quota_remaining -= 1
        db.commit()
    
        return challenge_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-history")
async def my_history(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Retrieves the challenge history for the authenticated user.
    
    Args:
        request (Request): The incoming request object.
        db (Session): The database session.
        
    Returns:
        List[Challenge]: A list of challenges created by the user.
    """
    user_details = authenticate_user(request)
    user_id = user_details.get("user_id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    challenges = get_user_challenges(db, user_id)
    
    return {"challenges": challenges}


@router.get("/quota")
async def get_quota(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Retrieves the challenge quota for the authenticated user.
    
    Args:
        request (Request): The incoming request object.
        db (Session): The database session.
        
    Returns:
        ChallengeQuota: The challenge quota for the user.
    """
    user_details = authenticate_user(request)
    user_id = user_details.get("user_id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    quota = get_challenge_quota(db, user_id)
    
    if not quota:
        return {
            "user_id": user_id,
            "quota_remaining": 0,
            "last_reset_date": datetime.now()
        }
    
    quota = reset_quota_if_needed(db, quota)
    
    return quota