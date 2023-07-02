from fastapi import FastAPI, APIRouter

from src.auth.routers import auth_router


app = FastAPI()

router = APIRouter(prefix="/v1")


router.include_router(auth_router)
app.include_router(router)