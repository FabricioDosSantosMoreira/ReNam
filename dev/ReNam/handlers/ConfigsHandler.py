import json

from typing import List, Any, Dict
from pathlib import Path


class ConfigHandler():

    def __init__(self, app) -> None:
        from Main import Main
        self.app: Main = app

        self.configs: Dict 

        # -=-=-=-=-=-= Interface =-=-=-=-=-=-
        self.input_msg: str

        self.min_interface_size: int
        self.max_string_length: int
        self.string_delimiter: str
        
        self.contents_pos: List[str]
        self.headers_pos: List[str]


        # -=-=-=-=-=-= DirectoryHandler() =--=-=-=-=-=-
        self.first_path_occurrence: bool

        self.num_of_processes: int

        self.excluded_paths: List[Path]
        self.drives: List[Path]

        self.selected_path: Path

        self.load_configs()


    def __str__(self) -> str:
        return (
            f"ConfigHandler(\n"
            f"  app={self.app},\n"
            f"  configs={self.configs},\n"
            f"  input_msg='{self.input_msg}',\n"
            f"  min_interface_size={self.min_interface_size},\n"
            f"  max_string_length={self.max_string_length},\n"
            f"  string_delimiter='{self.string_delimiter}',\n"
            f"  contents_pos={self.contents_pos},\n"
            f"  headers_pos={self.headers_pos},\n"
            f"  first_path_occurrence={self.first_path_occurrence},\n"
            f"  num_of_processes={self.num_of_processes},\n"
            f"  excluded_paths={self.excluded_paths},\n"
            f"  drives={self.drives},\n"
            f"  selected_path={self.selected_path}\n"
            f")"
        )


    def load_configs(self) -> None:
        json_path = Path('./ReNam/dev/ReNam/app/configs.json')
        try:
   
            with open(json_path, 'r', encoding='utf-8') as configs_file:
                self.configs = json.load(configs_file)

                self.input_msg = self.get_nested_config('interface', 'input_message')
                self.min_interface_size = self.get_nested_config('interface', 'min_interface_size')
                self.max_string_length = self.get_nested_config('interface', 'max_string_length')
                self.string_delimiter = self.get_nested_config('interface', 'string_delimiter')
                self.contents_pos = self.get_nested_config('interface', 'contents_pos')
                self.headers_pos = self.get_nested_config('interface', 'headers_pos')

                # Directory
                self.first_path_occurrence = self.get_nested_config('directory', 'first_path_occurrence')

                self.num_of_processes = self.get_nested_config('directory', 'num_of_processes')

                _temp = self.get_nested_config('directory', 'excluded_paths')
                if len(_temp) == 0:
                    self.excluded_paths = []
                else:
                    for i in range(len(_temp)):
                        self.excluded_paths.append(Path(_temp[i]))

                _temp = self.get_nested_config('directory', 'drives')
                if len(_temp) == 0:
                    self.drives = []
                else:
                    for i in range(len(_temp)):
                        self.drives.append(Path(_temp[i]))
               
                self.selected_path = Path(self.get_nested_config('directory', 'selected_path'))

        except json.decoder.JSONDecodeError as e:
            print(f"\nJSONDecodeError - - -> ['configs'] Weren't loaded. {e}.\n")
            


    def get_config(self, key) -> Any:
        return self.configs.get(key)
    
    def get_nested_config(self, nested_key, key) -> Any:

        nested_dict: Dict = self.get_config(nested_key)
        return nested_dict.get(key)


    def update(self) -> None:
        self.load_configs()



     
#    _____      _   _     
#   |  __ \    | \ | |                     
#   | |__) |___|  \| | __ _ _ __ ___       
#   |  _  // _ \ . ` |/ _` | '_ ` _ \      
#   | | \ \  __/ |\  | (_| | | | | | |     
#   |_|  \_\___|_| \_|\__,_|_| |_| |_|     
#            
