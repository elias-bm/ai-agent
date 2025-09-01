import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
from prompts import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

arg = sys.argv[1:]

def main():
    if not arg:
        print("Error. Please insert a question.")
        sys.exit(1)
    
    if "--verbose" in arg:
        arg.remove("--verbose")
        verbose = True
    else:
        verbose = False

    user_prompt = " ".join(arg)

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    if verbose:
        print(f"User prompt:" , user_prompt)
        print(f"Prompt tokens:" , response.usage_metadata.prompt_token_count)
        print(f"Response tokens:" , response.usage_metadata.candidates_token_count)
        print(response.text)

    else:
        print(response.text)

if __name__ == "__main__":
    main()
