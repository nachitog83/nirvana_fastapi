from fastapi import FastAPI
import uvicorn
from app.config import settings
from app.routers import router as app_router
import logging

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.include_router(app_router, tags=["root"])
    _app.include_router(app_router, tags=["insurance"])

    return _app


app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
        debug=settings.DEBUG_MODE,
    )
