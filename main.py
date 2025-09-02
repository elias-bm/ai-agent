import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

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

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
                               ]
        )
    
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=config,
    )

    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if hasattr(function_call_result.parts[0], "function_response"):
                if verbose==True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                raise ValueError("Doesn't exist.")


    elif verbose:
        print(f"User prompt:" , user_prompt)
        print(f"Prompt tokens:" , response.usage_metadata.prompt_token_count)
        print(f"Response tokens:" , response.usage_metadata.candidates_token_count)
        print(response.text)
    else:
        print(response.text)

if __name__ == "__main__":
    main()
