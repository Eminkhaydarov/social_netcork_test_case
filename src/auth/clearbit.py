from src.config import setting
import src.main as main

API_KEY = setting.CLEARBIT_API_KEY
URL = "https://person-stream.clearbit.com/v2/combined/find?email="


async def get_additional_data(email: str) -> dict:
    url = URL + email
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    async with main.aiohttp_session.get(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            person_data = data["person"]
            company_data = data["company"]
            location_data = person_data["location"]
            additional_data = {
                "full_name": person_data["name"]["fullName"],
                "location": location_data,
                "company": company_data["name"],
            }
            return additional_data
        return {}
