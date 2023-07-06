import uvicorn
from fastapi import FastAPI, APIRouter

from src.auth.routers import auth_router
from src.posts.routers import post_router


app = FastAPI()

router = APIRouter(prefix="/v1")


router.include_router(auth_router, tags=["Auth"])
router.include_router(post_router, tags=["posts"])
app.include_router(router)

def run_app():
    uvicorn.run(app)


if __name__ == "__main__":
    run_app()