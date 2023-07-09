import aiohttp
from fastapi import FastAPI, APIRouter

from src.auth.routers import auth_router
from src.posts.routers import post_router

app = FastAPI()

router = APIRouter(prefix="/v1")

router.include_router(auth_router, tags=["Auth"])
router.include_router(post_router, tags=["posts"])
app.include_router(router)


@app.get("/", status_code=200)
def index():
    return {"Hello": "World"}


aiohttp_session = None


@app.on_event("startup")
async def startup_event():
    global aiohttp_session
    aiohttp_session = aiohttp.ClientSession()


@app.on_event("shutdown")
async def shutdown_event():
    await aiohttp_session.close()
