from typing import List, Any
from wcwidth import wcswidth

from utils.any_utils import assign_distributed_list, ensure_value_parity
from utils.string_utils import has_non_ascii


def display_interface(
        contents_pos: List[str], 
        headers_pos: List[str], 
        contents: List[List[Any]], 
        headers: List[str], 
        min_interface_size: int, 
        use_last_col: bool = False
    ) -> str:


    # TODO: - check if this works
    #       - accept contents, headers as Any and transform to str
    headers_length = len(headers)
    contents_length = len(contents)
    
    
    # Create a List based on the size of 'len(headers)', Assigning integers representing lengths.
    # It can either distribute a value evenly or place a specific value at the end of the list
    distributed_str_sizes = assign_distributed_list(
                                value=min_interface_size, 
                                size=headers_length, 
                                assign_at_end=use_last_col)


    # Calculate each 'str_size' based on 'max_content_length' and change 'distributed_str_sizes' if necessary.
    for i in range(headers_length):
        str_size = 8  # Default size of 8 characters.

        # Get the maximum length of a content in contents.
        max_content_length = max(wcswidth(content[i]) for content in contents)

        # Add the largest value to 'str_size'.
        if max_content_length > len(headers[i]):
            str_size += max_content_length
        else:
            str_size += len(headers[i])

        # If the value calculated in 'assign_distributed_list' isn't enough, change to 'str_size'.
        if distributed_str_sizes[i] < str_size:
            distributed_str_sizes[i] = str_size


    # Calculate the necessary size for the last column
    if use_last_col:
        sizes_sum = sum(distributed_str_sizes) - distributed_str_sizes[-1]
        if distributed_str_sizes[-1] > max_content_length:
            distributed_str_sizes[-1] -= sizes_sum
            #distributed_str_sizes[-1] = max_content_length + 9

        if distributed_str_sizes[-1] < max_content_length + len(headers[-1]):
            distributed_str_sizes[-1] = max_content_length + len(headers[-1]) + 1 #- 8


    # Adjust the sizes in 'distributed_str_sizes' to ensure only even sizes, decreases by '1' if odd.
    for i in range(len(distributed_str_sizes)):
        distributed_str_sizes[i] = ensure_value_parity(distributed_str_sizes[i], target_parity="even", decrease=True)


    # Build 'border_str'.
    symbol_count_used: list = []
    border_str: str = "+"
    for i in range(headers_length): 
        for symbol_count in range(distributed_str_sizes[i]): 

            if (symbol_count % 2) == 0:
                border_str += '-'  # Add '-' for even indices
            else:
                border_str += '='  # Add '=' for odd indices

            if distributed_str_sizes[i] - 2 == symbol_count: 
                border_str += '+'  # add '+' if it is the end of the column

                # 'symbol_count_used' is used later
                symbol_count_used.append(symbol_count)  
                break


    # Build 'headers_string' based on 'headers_pos'.
    headers_string: str = "|"
    for i in range(headers_length):
        
        # If 'headers_pos[i]' isn't availiable, 'headers_pos[-1]' is used.
        try:
            pos = headers_pos[i]
        except IndexError:
            pos = headers_pos[-1]


        # 'headers[i]' Isn't an ASCII string
        visual_width = 0
        if has_non_ascii(headers[i]):
            visual_width = wcswidth(headers[i]) - len(headers[i])


        if pos == 'left':  
            width = symbol_count_used[i] - 2 - visual_width
            headers_string += f"   {headers[i].upper().ljust(width)}" + "|"

        elif pos == 'right':
            width = symbol_count_used[i] - 2 - visual_width
            headers_string += f"{headers[i].upper().rjust(width)}   " + "|"

        else:  # Default is 'center'.
            width = symbol_count_used[i] + 1 - visual_width
            headers_string += f"{headers[i].upper().center(width)}" + "|"


    # Build 'contents_str' based on 'contents_pos'.
    contents_str: str = ""
    for i in range(contents_length):
        contents_str += "|"

        for y in range(headers_length):

            # If 'contents_pos[i]' isn't availiable, 'contents_pos[-1]' is used.
            try:
                pos = contents_pos[y]
            except IndexError:
                pos = contents_pos[-1]

            # 'contents[i][y]' Isn't an ASCII string?
            visual_width = 0
            if has_non_ascii(contents[i][y]):
                visual_width = wcswidth(contents[i][y]) - len(contents[i][y])


            if pos == 'left':
                width = symbol_count_used[y] - 2 - visual_width 
                contents_str += f"   {contents[i][y].title().ljust(width)}" + "|"
    
            elif pos == "right":
                width = symbol_count_used[y] - 2 - visual_width 
                contents_str += f"{contents[i][y].title().rjust(width)}   " + "|"
                
            else:  # Default is 'center'.
                width = symbol_count_used[y] + 1 - visual_width
                contents_str += f"{contents[i][y].title().center(width)}" + "|"
        
        contents_str += "\n"


    print(border_str)
    print(headers_string)
    print(border_str)
    print(contents_str, end="")
    print(border_str)



def interface_msg(msg: str, size: int = 0):
    

    # Adjust size if it's less than the minimum required for the border and message
    size = max(len(msg) + 6, size)

    border_str: str = "+"

    if size % 2 != 0:
        remaining = 3
    else:
        remaining = 4

    # Build 'border_str'
    for symbol in range(size):  # Iterate through each index of 'str_sizes_list'

        if (symbol % 2) == 0:
            border_str += "-"  # Add "-" for even indices
        else:
            border_str += "="  # Add "=" for odd indices

        if size - remaining == symbol:  # If it is the end of the column
            border_str += "+"  # add "+"
            break

    print(border_str)
    print(f"|   {msg.ljust(size - remaining - 2)}" + "|")
