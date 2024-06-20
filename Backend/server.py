from fastapi import FastAPI  

app = FastAPI(
    title="RAG API",
    description="A Full-Stack RAG API",
    version="0.1",
)  

@app.get("/") 
async def index():     
  return {"message": "Hey, It is me Joshua.The server is running."}