from typing import List, Any, Dict
import json

class ConfigHandler():

    def __init__(self) -> None:
        self.configs: Dict 
        self.load_configs()

        # -=-=-=-=-=-= Interface =-=-=-=-=-=-
        self.input_msg: str

        self.min_interface_size: int
        self.max_string_length: int
        self.string_delimiter: str
        
        self.contents_pos: List[str]
        self.headers_pos: List[str]


    def load_configs(self) -> None:
        try:
            with open('ReNam/app/configs.json', 'r', encoding='utf-8') as configs_file:
                self.configs = json.load(configs_file)

        except json.decoder.JSONDecodeError as e:
            print(f"\nJSONDecodeError - - -> ['configs'] Weren't loaded. {e}.\n")
            
                        
    def get_config(self, key):
        return self.config_dict.get(key)







    def update_config(self, key, value):
        self.config_dict[key] = value



     
#    _____      _   _     
#   |  __ \    | \ | |                     
#   | |__) |___|  \| | __ _ _ __ ___       
#   |  _  // _ \ . ` |/ _` | '_ ` _ \      
#   | | \ \  __/ |\  | (_| | | | | | |     
#   |_|  \_\___|_| \_|\__,_|_| |_| |_|     
#            
