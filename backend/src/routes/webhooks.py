from http.client import HTTPException
from fastapi import APIRouter, HTTPException, Request, Depends
from ..database.db import create_challenge_quota
from ..database.models import get_db
from svix.webhooks import Webhook
import os
import json
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

@router.post("clerk")
async def handle_user_created(
    request: Request,
    db=Depends(get_db)
):
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
    
    if not webhook_secret:
        raise HTTPException(status_code=500, detail="CLERK_WEBHOOK_SECRET not configured")
    
    body = await request.body()
    payload = body.decode("utf-8")
    headers = dict(request.headers)
    
    try:
        wh = Webhook(webhook_secret)
        wh.verify(payload, headers)
        
        data = json.loads(payload)
        
        if data.get("type") != "user.created":
            return {"status": "ignored", "reason": "not user.created event"}
        
        user_data = data.get("data", {})
        user_id = user_data.get("id")
        
        create_challenge_quota(db, user_id)
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
