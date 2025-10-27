from fastapi import HTTPException
from fastapi import Header
import httpx


class UserClient:
    base_url: str = "http://auth-service:8000/auth"
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get_user_by_token(self, token: str = Header(None, alias="Authorization")):
        if not token:
            raise HTTPException(status_code=401, detail="Token not provided")

        try:
            response = await self.client.get(
                f"{self.base_url}/me",
                headers={"Authorization": token}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=401, detail="Invalid token")
