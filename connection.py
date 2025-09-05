import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# Load .env file
load_dotenv()

# Get GEMINI_API_KEY from environment
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY not found! Please set it in Railway Variables.")

# External client setup
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model configuration
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  # Tum latest Gemini model yaha rakh sakte ho
    openai_client=external_client
)

# Run config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
