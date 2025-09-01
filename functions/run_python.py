import os, subprocess, sys

def run_python_file(working_directory, file_path, args=[]):
    absolute_combined_path = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_working_directory = os.path.abspath(working_directory)
    inside = os.path.commonpath([absolute_working_directory, absolute_combined_path]) == absolute_working_directory
    
    if not inside:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_combined_path):
        return f'Error: File "{file_path}" not found.'
    if not absolute_combined_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            [sys.executable, file_path] + args,
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=working_directory,
        )

        out = completed_process.stdout or ""
        err =completed_process.stderr or ""

        if not out and not err:
            return "No output produced."
        
        result = f"STDOUT: {out}\nSTDERR: {err}"
        if completed_process.returncode != 0:
            result += f"\nProcess exited with code {completed_process.returncode}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    return result
