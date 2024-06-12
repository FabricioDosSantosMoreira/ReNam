import os
import re

from enum import Enum
from typing import Optional, Dict, List, Any, Union
from abc import ABC, abstractmethod
from pathlib import Path


class Midia(ABC):

    def __init__(self, app) -> None:
        from Main import Main

        self.app: Main = app

        self._title: str = ""

        self._file_extensions: List[Path] = []
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
    def file_extensions(self) -> List[Path]:
        return self._file_extensions

    @file_extensions.setter
    def file_extensions(self, value: Union[Path, List[Path]]) -> None:
        if isinstance(value, list):
            if all(isinstance(item, Path) for item in value):
                self._file_extensions = value
            else:
                raise ValueError("All items in the list 'value' must be of type 'Path'")
            
        elif isinstance(value, Path):
            self._file_extensions = [value]

        else:
            raise TypeError("Expected 'Path' or 'List[Path]'")

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

    def __init__(self, app, title: str) -> None:
        super().__init__(app=app)

        self.title = title

    
    def update(self):
        configs = self.app.configs


    def rename(self):
        print("\n\n\nrenaming movie")


class Series(Midia):

    def __init__(self, app, title: str) -> None:
        super().__init__(app=app)

        self.title = title

        self.season: int

        # Dict = {'key(episode_number)', item(episode_name)}
        self.episodes: Dict[int, str] = {}
    

    def extract_eps_order(files: List[Path], patterns: List[re.Pattern]) -> Dict[int, List[Path]]:
        # Dict = ["key(episode_number)", "item(["1p.1-file1", "ep.1-file1"], [...])"]

        file_order: dict[int, list[str]] = {}
        filtered_items = {}

        for pattern in patterns:
            for file in files:

                # re.search ask for str not Path
                match = re.search(pattern=pattern, string=str(file))

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


    def get_instance_of(self, app, *args, **kwargs) -> Union[Movie, Series]:
        _, cls = self.value
        return cls(app, *args, **kwargs)
    

    @classmethod
    def list_all(cls) -> List[str]:
        return list(map(lambda c: c.value[0], cls))


    def __str__(self):
        return f"{self.name} ({self.value})"


    def __repr__(self):
        return f"<MidiaEnum.{self.name}: {self.value}>"
    