from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from django.conf import settings # This points to your Django Project settings

def get_openai_api_key():
    # If need to fetch from DB for Multi Model execution/usage. When key stored in DB.
    return settings.OPENAI_API_KEY

def get_google_api_key():
    # If need to fetch from DB for Multi Model execution/usage. When key stored in DB.
    return settings.GOOGLE_API_KEY

def get_openai_model(model="gpt-4o-mini"):  # "gpt-4o-mini" will be default, if no input given
    return ChatOpenAI(
        model=model,
        temperature=0,
        # max_tokens=None,
        # timeout=None,
        max_retries=2,
        api_key=get_openai_api_key(),
        # base_url="...", # When we use ollama
        # organization="...",
        # other params...
    )
    
def get_google_model(model="gemini-2.0-flash-lite"):  # gemini-2.0-flash-lite gemini-2.5-flash
    # Initialize the Gemini model with the specified parameters
    if model is None:
        model = "gemini-2.0-flash-lite"
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0.0,
        max_retries=2,
        api_key=get_google_api_key(),
    )