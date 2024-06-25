import hashlib

import requests
import re
str_art = """
                _____      _   _
                |  __ \\    | \\ | |
                | |__) |___|  \\| | __ _ _ __ ___ 
                |  _  // _ \\ . ` |/ _` | '_ ` _ \\   
                | | \\ \\  __/ |\\  | (_| | | | | | | 
                |_|  \\_\\___|_| \\_|\\__,_|_| |_| |_|  
            """   

a = "S(\\d+)E(\\d+)"
print(type(a))

b = re.compile(a)
print(type(b))


re.compile("S(\\d+)E(\\d+)")
re.compile("s(\\d+)\\.e(\\d+)")
re.compile("EP\\.(\\d+)")