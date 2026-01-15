import os

import requests
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from dotenv import load_dotenv

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


