from collections import defaultdict
import os
import re

from enum import Enum
from typing import Optional, Dict, List, Any, Tuple, Union
from abc import ABC, abstractmethod
from pathlib import Path

from app.classes.handlers.directory_handler import DirectoryHandler


class BaseMidia(ABC):

    _file_extensions: List[str] = []
    _regex_patterns: List[re.Pattern] = []

    def __init__(self, app) -> None:
        from main import Main

        self.app: Main = app


    @abstractmethod
    def update(self) -> None: ...

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


class Movie(BaseMidia):

    def __init__(self, app) -> None:
        super().__init__(app=app)

        self.title: str
        self.launch_date: str

        self.update()


    def update(self) -> None:
        configs = self.app.config_handler

        # TODO: fix me
        self.file_extensions = ['.mp4', '.mkv']
        self.regex_patterns = [
            re.compile("S(\\d+)E(\\d+)"),
            re.compile("s(\\d+)\\.e(\\d+)"), 
            re.compile("EP\\.(\\d+)")
        ]


class Series(BaseMidia):

    _title: str = ""
    _season: str = ""
    #Dict = {episode_number: episode_name}
    _episodes: Dict[int, str] = {}

    def __init__(self, app) -> None:
        super().__init__(app=app)

        self.update()

    
    def update(self) -> None:
        configs = self.app.config_handler

        # TODO: fix me
        self.file_extensions = ['.mp4', '.mkv', '.zip', '.srt']
        a = re.compile(pattern="S(\\d+)E(\\d+)")
        b = re.compile(pattern="s(\\d+)\\.e(\\d+)")
        c = re.compile(pattern="EP\\.(\\d+)")
        d = re.compile(pattern="ep\\.(\\d+)")
        e = re.compile(pattern="EP(\\d+)")
        f = re.compile(pattern="Ep.(\\d+)")
        g = re.compile(pattern="S(\\d+) E(\\d+)")
        g1 = re.compile(pattern="ep(\\d+)")
        self.regex_patterns = [a,b,c,d,e, f, g, g1]


    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, title: str) -> None:
        self._title = title

    @property
    def season(self) -> str:
        return self._season
    
    @season.setter
    def season(self, season: str) -> None:
        if len(season) <= 1:
            season = f"0{season}"
        
        self._season = season

    @property
    def episodes(self) -> Dict[int, str]:
        return self._episodes
    
    @episodes.setter
    def episodes(self, episodes: Dict[int, str]) -> None:
        self._episodes = episodes


    def extract_eps_order(
            self, 
            files: List[str], 
            patterns: Optional[List[re.Pattern]] = None
        ) -> Tuple[Dict[int, List[Path]], int]:

        if patterns is None:
            patterns = self.regex_patterns
            
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


class Anime(BaseMidia):

    def __init__(self, app) -> None:
        super().__init__(app)

        self.title = "title"


class MidiasEnum(Enum):
    
    ANIME = ("Anime", Anime)
    MOVIE = ("Movie", Movie)
    SERIES = ("Series", Series)
    
    def get_instance(self, app, *args, **kwargs) -> Union[Anime, Movie, Series]:
        _, cls = self.value
        return cls(app, *args, **kwargs)
    
    @classmethod
    def list_all(cls) -> List[str]:
        return list(map(lambda c: c.value[0], cls))

    def __str__(self):
        return f"{self.name} ({self.value})"

    def __repr__(self):
        return f"<MidiaEnum.{self.name}: {self.value}>"
    