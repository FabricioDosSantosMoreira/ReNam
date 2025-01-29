import json

from typing import Callable, Union, List, Any, Dict
from pathlib import Path


class ConfigHandler:

    def __init__(self, app) -> None:
        from main import Main

        self.app: Main = app

        self.file = Path(__file__).resolve().parent.parent.parent.parent / "configs.json"

        self.update()

    
    def update(self) -> None:
        try:
            with open(file=self.file, mode='r', encoding='utf-8') as json_file:

                self.configs: Dict[str, Any] = json.load(json_file)

        except json.decoder.JSONDecodeError as exc:
            print(f"\nJSONDecodeError - - -> ['configs'] Weren't loaded. {exc}.\n")
        
        except Exception as exc:
            print(f"\nException - - -> ['configs'] Weren't loaded. {exc}.\n")

        # APIFetcher Configs
        key = 'api'

        self.api_key: str = self.get_config(key=key, nested_key='API_KEY')
        self.max_search: str = self.get_config(key=key, nested_key='MAX_SEARCH')

        # InterfaceHandler Configs
        key = 'interface'

        self.input_msg: str = self.get_config(key=key, nested_key='input_message')

        self.min_interface_size: int = self.get_config(key=key, nested_key='min_interface_size')
        self.max_string_length: int = self.get_config(key=key, nested_key='max_string_length')

        self.interface_symbols: Dict[str, str] = self.get_config(key=key, nested_key='interface_symbols')
        self.delimiter: str = self.get_config(key=key, nested_key='delimiter')

        self.headers_pos: List[str] = self.get_config(key=key, nested_key='headers_pos')
        self.contents_pos: List[str] = self.get_config(key=key, nested_key='contents_pos')

        _temp = self.get_config(key=key, nested_key='headers_func')
        self.headers_func: Callable[[str], str] = getattr(str, _temp, None)

        _temp = self.get_config(key=key, nested_key='contents_func')
        self.contents_func: Callable[[str], str] = getattr(str, _temp, None)


        # DirectoryHandler Configs
        key='directory'

        self.first_path_occurrence: bool = self.get_config(key=key, nested_key='first_path_occurrence')

        self.num_of_processes: int = self.get_config(key=key, nested_key='num_of_processes')
        self.max_path_results: int = self.get_config(key=key, nested_key='max_path_results')

        _temp = self.get_config(key=key, nested_key='excluded_paths')
        self.excluded_paths: List[Path] = [Path(p) for p in _temp] if _temp else []

        _temp = self.get_config(key=key, nested_key='drives')
        self.drives: List[Path] = [Path(d) for d in _temp] if _temp else []


        # Others Configs
        key = 'utils'

        self.welcome: List[str] = self.get_config(key=key, nested_key='welcome')


        # Midia Cofigs
        key = 'midia'
        self.extensions = self.get_config(key=key, nested_key='files_extensions')
        self.patterns = self.get_config(key=key, nested_key='regex_patterns')


    def get_config(self, key: str, nested_key: str) -> Union[Dict, Any]:

        return self.configs.get(key, {}).get(nested_key, None)
