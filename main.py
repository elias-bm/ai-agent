import os
import sys
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

arg = sys.argv[1:]

def main():
    if not arg:
        print("Error. Please insert a question.")
        sys.exit(1)
    
    question = " ".join(arg)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=question)
    print(response.text)
    print(f"Prompt tokens:" , response.usage_metadata.prompt_token_count)
    print(f"Response tokens:" , response.usage_metadata.candidates_token_count)   

if __name__ == "__main__":
    main()
