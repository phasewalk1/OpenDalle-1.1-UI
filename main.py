from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from diffusers import AutoPipelineForText2Image
from load_model import load_and_cache_model
import torch
from io import BytesIO
import base64

app = FastAPI()
origins = ["http://localhost:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

pipeline = AutoPipelineForText2Image.from_pretrained('dataautogpt3/OpenDalleV1.1', torch_dtype=torch.float16).to('cuda')

class ImageRequest(BaseModel):
    description: str


@app.on_event('startup')
async def startup_event():
    global pipeline
    print('Loading model from cache ...')
    pipeline = load_and_cache_model()

@app.post("/generate-image")
async def generate_image(request: ImageRequest):
    image = pipeline(request.description).images[0]
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return {"image": img_str}