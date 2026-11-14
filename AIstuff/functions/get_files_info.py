import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory:str, directory:str=".")-> str:

    try:
        wdirt = os.path.abspath(working_directory) #make the path the user inputs absolute( /home -> C/*some bullshit idk*/ home)
        dirt = os.path.join(wdirt, directory) #make whatever the ai wants to create a path after working directory (C: + /something -> C:/something)
        targ_dirt = os.path.normpath(dirt) #make sure the ai's directory isn't shtewpid (C:/./ or C:/somethinf/../)
        validity_dirt = os.path.commonpath([wdirt, targ_dirt]) == wdirt #make sure the ais path actually comes after the path we specified 
        
        if not validity_dirt: #if this ^ does some, and I quote, bullshit
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        
        if not os.path.isdir(targ_dirt): # if the target directory is on just some complete bullshit
            
            return f"Error: \"{directory}\" is not a directory"
    
        else: 
            files = os.listdir(targ_dirt) #make a list of all names of files in tag_dirt
            contents = f"Result for {directory} directory:\n" if directory != "." else f"Result for current directory:\n" #empty str which will have file infos
            try: 
                for i in files: #get da file infos
                    size = os.path.getsize(targ_dirt + "/" + i)
                    dirtBool = os.path.isdir(targ_dirt + "/" + i)
                    contents += f"- {i}: file_size={size} bytes, is_dir={dirtBool} \n"
            
            except Exception as E: # I frew up... again......
                raise Exception("Error: " + str(E))
            
            return contents

    except Exception as E: #mom... I frew up
        raise Exception("Error: " + str(E))
