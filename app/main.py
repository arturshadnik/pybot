from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import logger
from app.api.v1 import routes

logger.info("Starting server")
app = FastAPI()

app.middleware("http")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/v1", tags=[""])

@app.get('/health-check')
async def health_check():
    return {"status": "ok"}
