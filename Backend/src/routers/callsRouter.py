
from fastapi import APIRouter, Response, Request, status
from fastapi.responses import JSONResponse
from ..repository import calls
from .. import models

router = APIRouter(
    prefix="/api",
    tags=["Main Routes"],
)

@router.post("/chat",  status_code=status.HTTP_201_CREATED, description="Chat with the RAG API through this endpoint") 
async def Chat(message: models.Message):
    return await calls.Chat(message)

@router.post("/indexing", description="Index a website through this endpoint")
async def Indexing(url: models.Message):
    return await calls.Indexing(url)