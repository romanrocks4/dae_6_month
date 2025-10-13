import os
from pathlib import Path

def load_api_key():
    """Load API key from environment or .env file."""
    # Check environment variable first
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("Found API key in environment variable")
        print(f"API Key length: {len(api_key)} characters")
        return api_key
    
    # Check .env file in project root
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        print(f"Found .env file at {env_path}")
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    key = line.strip().split("=", 1)[1]
                    print("Found API key in .env file")
                    print(f"API Key length: {len(key)} characters")
                    # Print first and last few characters for verification (but not the full key)
                    if len(key) > 10:
                        print(f"API Key (first 5 and last 5 chars): {key[:5]}...{key[-5:]}")
                    return key
    
    print("No API key found")
    return None

if __name__ == "__main__":
    api_key = load_api_key()
    if api_key:
        # Don't print the full key for security reasons
        if len(api_key) < 39:
            print("Warning: API key seems too short to be valid (should be 39 characters)")
        else:
            print("API key appears to be of reasonable length")
    else:
        print("No API key found")
