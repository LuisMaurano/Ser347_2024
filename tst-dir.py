import os

current_directory = os.getcwd()
print(current_directory)

import pathlib
script_directory = pathlib.Path("pathdir.py").parent.resolve()
