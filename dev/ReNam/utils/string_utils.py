from typing import Optional, Tuple, List, Any, AnyStr


def reduce_string_length(
        *,
        string: str, 
        length: int, 
        delimiter: Optional[str], 
        end_cut: Optional[bool] = True,
    
    ) -> str:
    """
    Reduces the length of the given string to the specified length.

    Args:
        string (str): The string to be reduced.
        length (Optional[int]): The desired maximum length of the string after reduction.
        delimiter (Optional[str]): The delimiter to add between the reduced string and the omitted part.
        end_cut (Optional[bool]): If True, the reduction is done from the end of the string; 
            otherwise, it's done from the beginning. Defaults to True.

    Returns:
        str: 
            The reduced string.
    """

    # Check if 'length' is greater or equal to the string length. 
    # If so, return the string unaltered.
    if length >= len(string):  
        return string 
    
    delimiter = '' if delimiter is None else delimiter


    # If end_cut is True, reduce the string from its end.
    if end_cut:  
        return string[:length] + delimiter
    
    # If end_cut is False, reduce the string from its beginning.
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
            If False, returns a tuple containing False and -1, indicating the string is entirely ASCII.
            If True, returns a tuple containing True and the index of the first non-ASCII character found.
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
