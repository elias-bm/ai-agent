import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents="Why is the sky blue? Use one paragraph"
)

def main():
 print(response.text)
 print(f"Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
 print(f"Response tokens: " + str(response.usage_metadata.candidates_token_count))   

if __name__ == "__main__":
    main()
