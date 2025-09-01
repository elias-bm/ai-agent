import os

def write_file(working_directory, file_path, content):
    absolute_combined_path = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_working_directory = os.path.abspath(working_directory)
    inside = os.path.commonpath([absolute_working_directory, absolute_combined_path]) == absolute_working_directory
    
    if not inside:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    parent_directory = os.path.dirname(absolute_combined_path)
    os.makedirs(parent_directory, exist_ok=True)

    try:
        with open(absolute_combined_path, mode="w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: Failed to write in {file_path}: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
