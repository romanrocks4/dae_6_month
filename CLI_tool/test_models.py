import google.generativeai as genai
import os
from pathlib import Path

# Load API key from environment or .env file
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Check .env file in project root
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.strip().split("=", 1)[1]
                    break

if not api_key:
    print("GEMINI_API_KEY not found in environment variables or .env file")
    exit(1)

# Configure the API
genai.configure(api_key=api_key)

# List available models
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"Model: {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")