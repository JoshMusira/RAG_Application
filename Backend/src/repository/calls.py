from fastapi.responses import JSONResponse
from .. import models

async def Chat(message: models.Message):     
  return JSONResponse(content={"Message": message.message}, status_code=200)