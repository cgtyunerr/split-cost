"""Main project file."""
from fastapi import FastAPI

from app.middlewares import GenericErrorHandlerMiddleware

app: FastAPI = FastAPI(
    title="split cost API",
    description="Cost split API",
    version="0.1.0"
)
app.add_middleware(GenericErrorHandlerMiddleware)
