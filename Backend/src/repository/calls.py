from fastapi.responses import JSONResponse
from .. import models
from src.rag import get_answer_and_docs
from src.qdrant import upload_website_to_collection

async def Chat(message: models.Message):
    try:
        response = get_answer_and_docs(message.message)
        response_content = {
            "question": message.message,
            "answer": response["answer"],
            "documents": [doc.dict() for doc in response["context"]],
            "word_cloud_image": response["word_cloud_image"],
            "keywords": response["keywords"]
        }
        return JSONResponse(content=response_content, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

async def Indexing(url: models.Message):
    try:
        response = upload_website_to_collection(url.message)
        
        return JSONResponse(content={"response": response}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)