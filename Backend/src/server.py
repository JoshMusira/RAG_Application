from fastapi import FastAPI  
from fastapi.responses import JSONResponse
from  fastapi.middleware.cors import CORSMiddleware
from .routers import callsRouter

app = FastAPI(
    title="RAG API",
    description="A Full-Stack RAG API",
    version="0.1",
)  

origins = [
  "http://localhost:5173",
  "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
  
)

@app.get("/") 
async def index():     
  return {"message": "Hey, It is me Joshua.The server is running."}

app.include_router(callsRouter.router)