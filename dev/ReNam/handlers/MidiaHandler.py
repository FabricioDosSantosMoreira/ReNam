import os
import re

from typing import Optional, Dict, List, Any
from abc import ABC, abstractmethod
from pathlib import Path


class Midia(ABC):

    def __init__(self, app) -> None:
        from Main import Main

        self.app: Main = app
        
        self._name: str

        self._file_formats: List[str]
        self._regex_patterns: List[re.Pattern]


    @abstractmethod
    def rename():
        pass

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value


class Movie(Midia):

    def __init__(self, name: str) -> None:
        super().__init__(name=name)


    def rename():
        print('ranaming movie')


class Series(Midia):

    def __init__(self, name: str) -> None:
        super().__init__(name=name)

        self._season: int
    

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


    




    


