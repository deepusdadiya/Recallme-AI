from fastapi import FastAPI
from services.memory_pipeline.router import router as memory_router
from services.memory_query.router import router as query_router
from services.file_ingest.router import router as file_router
from services.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5173/dashboard"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(file_router, prefix="/api/file", tags=["File Upoload"])
app.include_router(memory_router, prefix="/api/memory", tags=["Memory Upload"])
app.include_router(query_router, prefix="/api/memory", tags=["QnA"])