import os, subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file in a specified directory relative to the working directory, doing so with the parameters specified",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to run files from, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list of strings",
                    "description": "The arguments passed onto the python file, default value is None",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    og_file_path = os.path.normpath(file_path)
    working_directory = os.path.abspath(working_directory)
    file_path = os.path.normpath(os.path.join(working_directory, file_path))


    if os.path.commonpath([working_directory, file_path]) != working_directory:
        return f"Error: Cannot execute \"{og_file_path}\" as it is outside the permitted working directory"
    
    try:
        if not os.path.isfile(file_path):
            return f'Error: "{og_file_path}" does not exist or is not a regular file'
    except Exception as E:
        return f"Error: {E}"

    if file_path.split(".")[-1] != "py":
        return f'Error: "{og_file_path}" is not a Python file'
    
    command = ["python", file_path]
    if not isinstance(args, type(None)):
        command.extend(args)

    try:

        output = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd = os.path.dirname(file_path))

        outstr = ""
        if output.returncode != 0:
            outstr += "Process exited with code X"
        if output.stdout == "" and output.stderr == "":
            outstr += "No output produced\n"
        else:
            outstr += "STDOUT: " + output.stdout + "\n"
            outstr += "STDERR: " + output.stderr + "\n"
        return outstr

    except Exception as E:
        return f"Error: executing Python file: {E}"

