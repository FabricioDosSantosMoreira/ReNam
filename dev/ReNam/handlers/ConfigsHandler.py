import json

from typing import List, Any, Dict
from pathlib import Path


class ConfigHandler():

    def __init__(self) -> None:
        self.configs: Dict 

        # -=-=-=-=-=-= Interface =-=-=-=-=-=-
        self.input_msg: str

        self.min_interface_size: int
        self.max_string_length: int
        self.string_delimiter: str
        
        self.contents_pos: List[str]
        self.headers_pos: List[str]

        self.load_configs()


    def load_configs(self) -> None:
        json_path = Path('./dev/ReNam/app/configs.json')
        try:

            with open(json_path, 'r', encoding='utf-8') as configs_file:
                self.configs = json.load(configs_file)

                self.input_msg = self.get_nested_config('interface', 'input_message')
                self.min_interface_size = self.get_nested_config('interface', 'min_interface_size')
                self.max_string_length = self.get_nested_config('interface', 'max_string_length')
                self.string_delimiter = self.get_nested_config('interface', 'string_delimiter')
                self.contents_pos = self.get_nested_config('interface', 'contents_pos')
                self.headers_pos = self.get_nested_config('interface', 'headers_pos')

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
