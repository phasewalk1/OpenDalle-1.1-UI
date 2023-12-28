from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
from typing import Optional
from diffusers import AutoPipelineForText2Image
import base64
import logging

from scripts.load_model import load_and_cache_model

app = FastAPI()
origins = ["http://localhost:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

pipeline = None

class ImageRequest(BaseModel):
    description: str

@app.on_event('startup')
async def startup_event():
    global pipeline
    print('Loading model from cache ...')
    pipeline = load_and_cache_model()

@app.post("/generate-image")
async def generate_image(request: ImageRequest):
    try:
        logger.info('Generating image w/ prompt: ', request.description)
        if (pipeline != None):
            image = pipeline(request.description).images[0]
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return {"image": img_str}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

