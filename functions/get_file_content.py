import os
from functions.config import *

def get_file_content(working_directory, file_path):
    absolute_combined_path = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_working_directory = os.path.abspath(working_directory)
    inside = os.path.commonpath([absolute_working_directory, absolute_combined_path]) == absolute_working_directory
    
    if not inside:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_combined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open (absolute_combined_path, mode="r") as f:
            chunk = f.read(MAX_CHARS + 1)
            if len(chunk) > MAX_CHARS:
                file_content = f'{chunk[:MAX_CHARS]}[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            else:
                file_content = chunk
    except Exception as e:
        return f'Error: Failed to read file content for "{file_path}": {e}'

    return file_content