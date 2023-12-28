from diffusers import AutoPipelineForText2Image
import torch

def load_and_cache_model():
    """
    Load the OpenDalleV1.1 model from the local directory and return the pipeline.
    """
    try:
        # Load the model from the local directory
        model_path = './OpenDalleV1.1'  # Adjust the path if your model is in a different directory
        pipeline = AutoPipelineForText2Image.from_pretrained(model_path).to('cpu')
        print("Model loaded successfully.")
        return pipeline
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

