import hashlib
import os
from typing import Annotated

import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv
from .model.snippet import User

load_dotenv()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
ALGORITHM = os.getenv("KEYCLOAK_HASH_ALGORITHM")

security = HTTPBearer()


class AuthHandler:
    def __init__(self):
        self.jwks_url = f"{KEYCLOAK_URL}/protocol/openid-connect/certs"
        self.jwks = None

    def get_public_key(self):
        if self.jwks is None:
            try:
                response = requests.get(self.jwks_url)
                response.raise_for_status()
                self.jwks = response.json()
            except Exception as e:
                print(f"Chyba při stahování klíčů z Keycloaku: {e}")
                raise HTTPException(status_code=500, detail="Auth service unavailable")
        return self.jwks

    def verify_token(self, token: str):
        jwks = self.get_public_key()

        try:
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}

            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }

            if not rsa_key:
                self.jwks = None
                raise JWTError("Key not found")

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=[ALGORITHM],
                options={
                    "verify_aud": False,
                    "verify_iss": False
                }
            )

            return payload

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
            )


auth_handler = AuthHandler()


async def get_current_user_allow_none(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> User | None:
    token = credentials.credentials
    payload = auth_handler.verify_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        return None

    email_bytes = payload.get("email").strip().lower().encode('utf-8')

    return User(
        id=user_id,
        username=payload.get("preferred_username"),
        email_hash=hashlib.md5(email_bytes).hexdigest(),
    )


async def get_current_user(user: Annotated[User | None, Depends(get_current_user_allow_none)]) -> User:
    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="Token missing user ID"
        )
    return user
