from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

# model = genai.GenerativeModel("gemini-pro")


def generate_response(prompt: str):
    if not prompt:
        raise ValueError("Prompt is empty")
    
    # Use a supported text generation model. If this still errors, run a small
    # script to call `client.list_models()` and pick a model from the result.
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
    )

    # Return raw response string for debugging; later update to parse structured content.
    return response.text