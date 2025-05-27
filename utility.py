from os import getcwd as _getcwd

def convertFileName(filepath:str): # use windows filepath
    # Get file path type
    if "D:" in _getcwd():
        try:
            file_test = "Big-oAnimals/"+'save.txt'.replace("\\", "/")
            with open(file_test, 'r') as _:
                pass
            file_path_type = "Big-oAnimals/"
        except:
            file_test = 'save.txt'.replace("\\", "/")
            print(f"File test: {file_test}")
            with open(file_test, 'r') as _:
                pass
            file_path_type = _getcwd().split("/")[-1]
    
    # Change file name
    if 'C:' in _getcwd():
        return filepath
    elif 'D:' in _getcwd():
        return file_path_type + filepath.replace("\\", "/")
    else:
        return _getcwd()+"/"+filepath.replace("\\", "/")