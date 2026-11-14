import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads files in a specified directory relative to the working directory, providing file contents as a string",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to read files from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    file_path = os.path.join(working_directory, file_path)
    try:
        if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(file_path)]) != os.path.abspath(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as E:
        return f"Error: {E}"
    try:
        with open(file_path) as file:
            file_str = file.read(MAX_CHARS)
            if len(file_str) >= MAX_CHARS:
                file_str += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_str
    except Exception as E:
        return f"Error: {E}"
    

