from typing import List

def reduce_str_length(
        string: str, 
        *, 
        length: int = 30, 
        delimiter: str = '', 
        end_cut: bool = True,
        ) -> str:

    # Is 'length' greater or equal to string length? If so return the string.
    if length >= len(string):  
        return string 

    # Is end_cut True? If so return a string with a cut on its ending
    if end_cut:  
        return string[:length] + delimiter
    
    # Otherwise, return a string with a cut at its start.
    return delimiter + string[-length:]


def reduce_list_of_str_length(
        list_of_strings: List[str], 
        *, 
        length: int = 30, 
        delimiter: str = "", 
        end_cut: bool = True,
        ) -> list[str]:

    for i, string in enumerate(list_of_strings):
        list_of_strings[i] = reduce_str_length(string, length=length, delimiter=delimiter, end_cut=end_cut)

    return list_of_strings


def has_non_ascii(string: str) -> bool:
    for char in string:
        if ord(char) > 127:
            return True
        
    return False
