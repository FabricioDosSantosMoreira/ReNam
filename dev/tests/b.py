from pathlib import Path
import sys

# NOTE: Add src to sys.path
SRC_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(SRC_PATH))

print(SRC_PATH)
from dev.ReNam.utils.string_utils import *
from dev.ReNam.utils.generic_utils import *

