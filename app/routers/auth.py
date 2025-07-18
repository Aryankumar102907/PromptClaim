import os
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import RedirectResponse
import httpx
from jose import jwt
from datetime import timedelta

from core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import create_access_token

router = APIRouter()

@router.get("/google")
async def google_auth():
    scope = "openid profile email"
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"scope={scope}&"
        f"access_type=offline"
    )
    return RedirectResponse(google_auth_url)

@router.get("/google/callback")
async def google_auth_callback(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=token_data)
    response.raise_for_status()
    tokens = response.json()

    id_token = tokens["id_token"]
    user_info = jwt.decode(id_token, key=None, audience=GOOGLE_CLIENT_ID, options={"verify_signature": False, "verify_at_hash": False})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_info["email"], "name": user_info.get("name"), "picture": user_info.get("picture")},
        expires_delta=access_token_expires
    )
    # Redirect to frontend with token
    return RedirectResponse(url=f"http://localhost:3000?token={access_token}")
