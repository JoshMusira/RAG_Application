
from fastapi import APIRouter, Response, Request, status
from fastapi.responses import JSONResponse

from src.visuals import plot_source_urls, detailed_joe_biden_articles_sentiment, plot_sentiment_polarity_distribution
from src.totalsources import get_newsapi_sources
from ..repository import calls
from .. import models
from .. import qdrant
from .. import newsapi
from pydantic import BaseModel
from datetime import datetime
from typing import Dict

router = APIRouter(
    prefix="/api",
    tags=["Main Routes"],
)

class CollectionRequest(BaseModel):
    collectionName: str

class NewsRequest(BaseModel):
    names: str
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

@router.post("/chat-combined",  status_code=status.HTTP_201_CREATED, description="Chat with the RAG API through this combined endpoint") 
async def Chat(message: models.Message):
    return await calls.ChatCombined(message)

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
        url = request_body.names
        start_date = datetime.strptime(request_body.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(request_body.end_date, '%Y-%m-%d')
        newsapi.upload_news_to_collection(url, start_date, end_date)
        return JSONResponse(content={"message": "News articles uploaded successfully"}, status_code=status.HTTP_201_CREATED)
    except ValueError:
        return JSONResponse(content={"message": "Invalid date format. Use YYYY-MM-DD"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error in upload_news: {e}")
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/upload_news_combined", description="Upload news articles to a combined collection")
async def upload_news(request_body: NewsRequest):
    try:
        url = request_body.names
        start_date = datetime.strptime(request_body.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(request_body.end_date, '%Y-%m-%d')
        newsapi.upload_news_to_collection_new(url, start_date, end_date)
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
    

@router.get("/count-unique-urls-combined", description="Count the number of combined unique URLs in the collection")
async def count_combined_unique_urls_route():
    try:
        result = qdrant.count_unique_urls_combined()
        return JSONResponse(content={"message": result}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error in count_unique_urls_route: {e}")
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/news-sources")
def news_sources():
    sources = get_newsapi_sources()
    return {"sources": sources}

@router.get("/plots", response_model=Dict[str, str])
async def get_plots():
    source_url_img = plot_source_urls(detailed_joe_biden_articles_sentiment)
    sentiment_polarity_img = plot_sentiment_polarity_distribution(detailed_joe_biden_articles_sentiment)
    return {"source_url_image": source_url_img, "sentiment_polarity_image": sentiment_polarity_img}

