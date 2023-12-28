from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import subprocess
import base64

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ImageRequest(BaseModel):
    description: str

@app.post("/generate-image")
async def generate_image(request: ImageRequest):
    try:
        logger.info(f'Generating image w/ prompt: {request.description}')
        # Run the Python script with the provided description
        subprocess.run(["python", "scripts/infer.py", request.description], check=True)

        # Read the generated image
        with open("image.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        return {"image": encoded_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
