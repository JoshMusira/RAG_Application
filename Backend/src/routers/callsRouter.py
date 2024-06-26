
from fastapi import APIRouter, Response, Request, status
from fastapi.responses import JSONResponse
from ..repository import calls
from .. import models
from .. import qdrant
from .. import newsapi
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/api",
    tags=["Main Routes"],
)

class CollectionRequest(BaseModel):
    collectionName: str

class NewsRequest(BaseModel):
    url: str
    start_date: str
    end_date: str

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


@router.post("/upload_news", description="Upload news articles to a collection")
async def upload_news(request_body: NewsRequest):
    try:
        url = request_body.url
        start_date = datetime.strptime(request_body.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(request_body.end_date, '%Y-%m-%d')
        newsapi.upload_news_to_collection(url, start_date, end_date)
        return JSONResponse(content={"message": "News articles uploaded successfully"}, status_code=status.HTTP_201_CREATED)
    except ValueError:
        return JSONResponse(content={"message": "Invalid date format. Use YYYY-MM-DD"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error in upload_news: {e}")
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/count-unique-urls", description="Count the number of unique URLs in the collection")
async def count_unique_urls_route():
    try:
        result = qdrant.count_unique_urls()
        return JSONResponse(content={"message": result}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error in count_unique_urls_route: {e}")
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
