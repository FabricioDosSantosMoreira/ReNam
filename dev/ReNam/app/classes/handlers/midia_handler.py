from collections import defaultdict
import os
import re

from enum import Enum
from typing import Optional, Dict, List, Any, Union
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
        configs = self.app.configs

        self.file_extensions = ['.mp4', '.mkv']
        self.regex_patterns = [
            re.compile("S(\\d+)E(\\d+)"),
            re.compile("s(\\d+)\\.e(\\d+)"), 
            re.compile("EP\\.(\\d+)")
        ]



    def rename(self, files: List[Path], info: List[str]):

        name: str = f"{info[1]} - {info[2]}"

        breakpoint()
        print("\n\n\nrenaming movie")
        files = DirectoryHandler.filter_files(files=files, formats=self.file_extensions)
        breakpoint()
        for i, file in enumerate(files):
            os.rename(
                src=file,
                dst=f"{file.parent}/{name}.{file.suffix}"    
            )







class Series(Midia):

    def __init__(self, app) -> None:
        super().__init__(app=app)

        self.title = ""

        self.season: int

        # Dict = {'key(episode_number)', item(episode_name)} da API
        self.episodes: Dict[int, str] = {}


        self.update()
    

    def update():
        pass

    def extract_eps_order(files: List[Path], patterns: List[re.Pattern]) -> Dict[int, List[Path]]:
        # Dict = ["key(episode_number)", "item(["ep.1-file1", "ep.1-file2"], [...])"]

        #episode_files: Dict[int, List[Path]] = defaultdict(list)
        file_order: dict[int, list[str]] = {}
        filtered_items = {}

        

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
                                break
                            except KeyError:
                                file_order[order]  = []


                    except AttributeError:
                        print("\nERROR - - -> AtributeError.")
                    except ValueError:
                        print("\nERROR - - -> ValueError.")

            if file_order:
                filtered_items = dict(sorted(file_order.items()))

        return filtered_items 
    

    def rename(start_from: int, end_at: int) -> None:

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
    