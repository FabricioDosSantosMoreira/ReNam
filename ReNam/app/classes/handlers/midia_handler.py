from collections import defaultdict
import os
import re

from enum import Enum
from typing import Optional, Dict, List, Any, Tuple, Union
from abc import ABC, abstractmethod
from pathlib import Path

from app.classes.handlers.directory_handler import DirectoryHandler


class Midia(ABC):

    def __init__(self, app) -> None:
        from main import Main

        self.app: Main = app

        self._title: str = ""

        self._file_extensions: List[str] = []
        self._regex_patterns: List[re.Pattern] = []

    @abstractmethod
    def rename():
        pass

    @abstractmethod
    def update():
        pass

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def file_extensions(self) -> List[str]:
        return self._file_extensions

    @file_extensions.setter
    def file_extensions(self, value: Union[str, List[str]]) -> None:
        if isinstance(value, list):
            if all(isinstance(item, str) for item in value):
                self._file_extensions = value
            else:
                raise ValueError("All items in the list 'value' must be of type 'str'")
            
        elif isinstance(value, str):
            self._file_extensions = [value]

        else:
            raise TypeError("Expected 'Path' or 'List[str]'")

    @property
    def regex_patterns(self) -> List[re.Pattern]:
        return self._regex_patterns
    
    @regex_patterns.setter
    def regex_patterns(self, value: Union[re.Pattern, List[re.Pattern]]) -> None:
        if isinstance(value, list):
            if all(isinstance(item, re.Pattern) for item in value):
                self._regex_patterns = value
            else:
                raise ValueError("All items in the list 'value' must be of type 're.Pattern'")
        
        elif isinstance(value, re.Pattern):
            self._regex_patterns = [value]

        else:
            raise TypeError("Expected 're.Pattern' or 'List[re.Pattern]'")


class Movie(Midia):

    def __init__(self, app) -> None:
        super().__init__(app=app)

        self.title = ""

        self.update()

    
    def update(self):
        configs = self.app.config_handler

        self.file_extensions = ['.mp4', '.mkv']
        self.regex_patterns = [
            re.compile("S(\\d+)E(\\d+)"),
            re.compile("s(\\d+)\\.e(\\d+)"), 
            re.compile("EP\\.(\\d+)")
        ]


    def rename(self, files: List[Path], info: List[str]):

        name: str = f"{info[1]} - {info[2]}"

        files = DirectoryHandler.filter_files(files=files, formats=self.file_extensions)
        for i, file in enumerate(files):
            dst = Path(f"{file.parent}/{name}.{file.suffix}")
            os.rename(
                src=file,
                dst=dst    
            )
            print(f"\nRenamed ['{file}'] to ['{dst}']")


class Series(Midia):

    def __init__(self, app) -> None:
        super().__init__(app=app)

        self.title = ""

        self.season: int

        # Dict = {'key(episode_number)', item(episode_name)} da API
        self.episodes: Dict[int, str] = {}


        self.update()
    

    def update(self):
        self.file_extensions = ['.mp4', '.mkv']

        a = re.compile(pattern="S(\\d+)E(\\d+)")
        b = re.compile(pattern="s(\\d+)\\.e(\\d+)")
        c = re.compile(pattern="EP\\.(\\d+)")
        d = re.compile(pattern="ep\\.(\\d+)")
        e = re.compile(pattern="EP(\\d+)")
        self.regex_patterns = [a,b,c,d,e]


    def extract_eps_order(self, files: List[Path], patterns: List[re.Pattern]) -> Tuple[Dict[int, List[Path]], int]:
        # Dict = ["key(episode_number)", "item(["ep.1-file1", "ep.1-file2"], [...])"]

        #episode_files: Dict[int, List[Path]] = defaultdict(list)
        file_order: dict[int, list[str]] = {}
        filtered_items = {}
        total = 0

        for pattern in patterns:
            for file in files:

                # 're.search' asks for a 'str' not 'Path'
                file = str(file) # Path.as_posix() doesn't work here
                match = re.search(pattern=pattern, string=file)

                # Talvez de para utilizar o fromkeys que define um valor padrao para cada key

                # ou o dict.get que não lança key error, mas retorna none ou um valor default
                # Ex meu_dict.get("chave", valor_padrao_aq)
                if match:
                    print("match!!!", file)
                    try:
                        order = int(match.group(match.lastindex))
                        while True: # Talvez n precise???
                            try:
                                file_order[order].append(file)
                                total += 1
                                break
                            except KeyError:
                                file_order[order]  = []


                    except AttributeError:
                        print("\nERROR - - -> AtributeError.")
                    except ValueError:
                        print("\nERROR - - -> ValueError.")

            if file_order:
                filtered_items = dict(sorted(file_order.items()))

        return filtered_items, total    

    def rename(self, files: List[Path], info: List[str]) -> None:
        
        root_path: Path = files[0].parent
        files_name: List[str] = self.app.directory_handler.get_path_name(files)


        result, total_results = self.extract_eps_order(files=files_name, patterns=self.regex_patterns)
        if total_results != len(files):
            print(f"\n'extract_eps_order' dindn''t work.")
            return None

        episodes_info: List[str] = []
        for i, episode in enumerate(info):
            episodes_info.append(f"{episode[0]} S{episode[2]} EP{episode[1]}")
        
        episodes, total_results = self.extract_eps_order(files=episodes_info, patterns=[re.compile("EP(\\d+)")])
        if total_results != len(episodes_info):
            print(f"\n'extract_eps_order' dindn''t work.")
            return None


        new_names: List = []
        for key in result.keys():
            name = episodes.get(key, [])[0]
            if name:
                new_names.append(name)

        episodes, total_results = self.extract_eps_order(files=new_names, patterns=[re.compile("EP(\\d+)")])
        if total_results != len(result):
            print(f"\n'extract_eps_order' dindn''t work.")
            return None


        if len(result) != len(episodes):
            print(f"not enough correspondencies")
            return None


        old_paths: List[Path] = []
        new_paths: List[Path] = []
        old_names: List[str] = []
        new_names: List[str] = []
        for key, values in result.items():
            for value in values:
                old_name = self.app.directory_handler.get_path_name(paths=[value])[0]
                suffix = self.app.directory_handler.get_path_suffix(paths=[old_name])[0]
                new_name = f"{self.title} - {episodes.get(key, [])[0]}{suffix}"

                old_path = Path(root_path / old_name)
                new_path = Path(root_path / new_name)

                old_paths.append(old_path)
                new_paths.append(new_path)
                old_names.append(old_name)
                new_names.append(new_name)

        if len(old_paths) != len(new_paths):
            print("Couldn't rename. Missing paths correspondencies")

        interface = self.app.interface_handler

        HEADERS = ["OLD FILE NAMES", "NEW FILES NAMES"]
        CONTENTS = []
        for i in range(len(old_paths)):
            CONTENTS.append([old_names[i], new_names[i]])

        interface.display_interface(headers=HEADERS, contents=CONTENTS)
        value = input("press y to rename, else cancel: ")

        if str(value).lower() == "y":
            for i in range(len(old_paths)):
                if old_paths[i].exists():
                    os.rename(old_paths[i], new_paths[i])
                else:
                    print(f"{old_paths[i]} does not exist")

         














class Anime(Midia):
    pass


class MidiaEnum(Enum):
    
    MOVIE = ("Movie", Movie)
    SERIES = ("Series", Series)


    def get_instance(self, app, *args, **kwargs) -> Union[Movie, Series]:
        _, cls = self.value
        return cls(app, *args, **kwargs)
    

    @classmethod
    def list_all(cls) -> List[str]:
        return list(map(lambda c: c.value[0], cls))


    def __str__(self):
        return f"{self.name} ({self.value})"


    def __repr__(self):
        return f"<MidiaEnum.{self.name}: {self.value}>"
    