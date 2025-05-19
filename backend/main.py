from fastapi import FastAPI
from services.memory_pipeline.router import router as memory_router

app = FastAPI()

app.include_router(memory_router, prefix="/api/memory")