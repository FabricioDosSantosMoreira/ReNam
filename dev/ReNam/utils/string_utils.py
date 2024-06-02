from typing import Tuple, List, Any, AnyStr

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


def has_non_ascii(string: str) -> Tuple[bool, int]:
    """
    Check if a string contains non-ASCII characters.

    Args:
        string (str): The string to be checked.

    Returns:
        Tuple[bool, int]: 
            - If False, returns a tuple containing False and -1, indicating the string is entirely ASCII.
            - If True, returns a tuple containing True and the index of the first non-ASCII character found.
    """

    # If the string is entirely ASCII, return False.
    if string.isascii(): 
        return False, -1
    
    for i, char in enumerate(string):
        # Check if the ordinal value of the character is greater than 127,
        # indicating it's a non-ASCII character.
        if ord(char) > 127:
            return True, i
        
        
    return False, -1
