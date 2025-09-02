import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
from prompts import *
from functions.get_files_info import schema_get_files_info

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

    available_functions = types.Tool(function_declarations=[schema_get_files_info,])
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=config,
    )

    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    elif verbose:
        print(f"User prompt:" , user_prompt)
        print(f"Prompt tokens:" , response.usage_metadata.prompt_token_count)
        print(f"Response tokens:" , response.usage_metadata.candidates_token_count)
        print(response.text)
    else:
        print(response.text)

if __name__ == "__main__":
    main()
