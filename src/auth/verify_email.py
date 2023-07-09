from fastapi import HTTPException
from starlette import status
import src.main as main
from src.config import setting

API_KEY = setting.EMAILHUNTER_API_KEY
URL = "https://api.hunter.io/v2/email-verifier"


async def verify_email(email: str) -> bool:
    url = URL + f"?email={email}&api_key={API_KEY}"
    async with main.aiohttp_session.get(url) as response:
        resp = await response.json()
        if response.status == 200:
            if resp["data"]["status"] == "valid":
                return True
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {email} is not valid",
                )
        else:
            return False
