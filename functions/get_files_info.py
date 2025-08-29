import os

def get_files_info(working_directory, directory="."):
    combined_path = os.path.join(working_directory, directory)
    absolute_combined_path = os.path.abspath(combined_path)
    absolute_working_directory = os.path.abspath(working_directory)

    if not absolute_combined_path.startswith(absolute_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(absolute_combined_path):
        return f'Error: "{directory}" is not a directory'

    information = []
    content_list = os.listdir(absolute_combined_path)
    for item in content_list:
        item_path = os.path.join(absolute_combined_path, item)
        try:
            size = os.path.getsize(item_path)
            directory_statement = os.path.isdir(item_path)
        except Exception as e:
            return f"Error: Failed to process {item_path}: {e}"
        information.append(f"- {item}: file_size={size} bytes, is_dir={directory_statement}")
    return "\n".join(information)
