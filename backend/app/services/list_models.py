from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def list_models():
    for model in client.models.list():
        print(model.name)

if __name__ == "__main__":
    list_models()
