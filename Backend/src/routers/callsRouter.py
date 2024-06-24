
from fastapi import APIRouter, Response, Request, status
from fastapi.responses import JSONResponse
from ..repository import calls
from .. import models
from .. import qdrant
from pydantic import BaseModel

router = APIRouter(
    prefix="/api",
    tags=["Main Routes"],
)

class CollectionRequest(BaseModel):
    collectionName: str

# @router.websocket("/async_chat")
# async def async_chat(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         question = await websocket.receive_text()
#         await websocket.send_text(data)
   

@router.post("/chat",  status_code=status.HTTP_201_CREATED, description="Chat with the RAG API through this endpoint") 
async def Chat(message: models.Message):
    return await calls.Chat(message)

@router.post("/indexing", description="Index a website through this endpoint")
async def Indexing(url: models.Message):
    return await calls.Indexing(url)

@router.post("/delete-collection-content", status_code=status.HTTP_200_OK, description="Delete content of a collection")
async def delete_collection_content_route(request_body: CollectionRequest):
    try:
        collection_name = request_body.collectionName
        print(f"Received request to delete content of collection: {collection_name}")
        result = qdrant.delete_collection_content(collection_name)
        return JSONResponse(content={"message": result}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error in delete_collection_content_route: {e}")
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
