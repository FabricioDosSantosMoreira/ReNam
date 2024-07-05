from enum import Enum
import re
from typing import Dict


class DynamicPatternEnum():

    def __init__(self, **kwargs: Dict[str, re.Pattern]):
        self.values: Dict[str, re.Pattern] = kwargs


    def __getattr__(self, item: str):
        if item in self.values:
            return self.values[item]
        
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")


    def add_value(self, name: str, value: re.Pattern):
        if name not in self.values:
            self.values[name] = value
        else:
            raise ValueError(f"Value '{name}' already exists in enum")
 

# Exemplo de uso:
p1 = re.compile(pattern="S(\\d+)E(\\d+)")
p2 = re.compile(pattern="s(\\d+)\\.e(\\d+)")

my_enum = DynamicPatternEnum(PATTERN1=p1, PATTERN2=p2)


# # Adicionando novos valores dinamicamente
p3 = re.compile(pattern="S(\\d+)E(\\d+)")
p4 = re.compile(pattern="s(\\d+)\\.e(\\d+)")
my_enum.add_value('PATTERN3', p3)
my_enum.add_value('PATTERN4', p4)


print(my_enum.PATTERN1)  # Saída: value1
print(my_enum.PATTERN2)  # Saída: value2
print(my_enum.PATTERN3)  # Saída: value3
print(my_enum.PATTERN4)  # Saída: value4



print(my_enum.values)


# a ideia é ter uma key para o Dict e uma tupla com o pattern e a descrição
# values: Dict[str, Tuple(re.Pattern, str)]
# values["PATTERN1"] = (re.compile("algo"), "Default pattern for Animes")