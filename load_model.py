from diffusers import AutoPipelineForText2Image
import torch

def load_and_cache_model(model_name='dataautogpt3/OpenDalleV1.1', device='cuda'):
    pipeline = AutoPipelineForText2Image.from_pretrained(model_name, torch_dtype=torch.float16).to(device)
    return pipeline

if __name__ == "__main__":
    print("Loading and caching the model...")
    load_and_cache_model()
    print("Model loaded and cached successfully.")