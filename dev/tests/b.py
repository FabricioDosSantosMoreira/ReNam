from pathlib import Path
import sys

# NOTE: Add src to sys.path
SRC_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(SRC_PATH))

# print(SRC_PATH)
# from dev.ReNam.utils.string_utils import *
# from dev.ReNam.utils.generic_utils import *

# print(len("+-=-=-=-=-=-=-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+"))

from dev.ReNam.handlers.DirectoryHandler import DirectoryHandler
from pathlib import Path
from typing import List, Union

p = Path("D:\\Filmes, Séries e Animes\\Animes\\Akame Ga Kill")
paths = DirectoryHandler.get_directory_files(p)

a = DirectoryHandler.filter_files(paths, ['.mp4'])


print(a)
print(len(a))