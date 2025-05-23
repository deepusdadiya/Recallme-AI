from fastapi import FastAPI
from services.memory_pipeline.router import router as memory_router
from services.memory_query.router import router as query_router
from services.file_ingest.router import router as file_router

app = FastAPI()

app.include_router(memory_router, prefix="/api/memory")
app.include_router(query_router, prefix="/api/memory")
app.include_router(file_router, prefix="/api/file")