import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes files in a specified directory relative to the working directory, returning a string declaring its success or lack thereof",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to list files from, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "The contents which will be writen to the file specified in the directory parameter",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_directory = os.path.abspath(working_directory)
    file_path = os.path.normpath(os.path.join(working_directory, file_path))
    if os.path.commonpath([working_directory, file_path]) != working_directory:
        return f"Error: Cannot write \"{file_path}\" as it is outside the permitted working directory"
    
    if os.path.isdir(file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        with open(file_path, mode = "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as E:
        return f"Error: {E}"