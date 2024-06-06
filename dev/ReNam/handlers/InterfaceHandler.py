from typing import Callable, Optional, Dict, List, Any, Tuple, Union
from wcwidth import wcswidth
from time import sleep

from utils.generic_utils import match_parity, evenly_assign_value_to_list
from utils.string_utils import has_non_ascii
from utils.input_utils import read_int


class InterfaceHandler():

    def __init__(self, app) -> None:
        from Main import Main

        self.app: Main = app

        self.contents_pos: List[str]
        self.headers_pos: List[str]

        self.min_interface_size: int
        self.max_string_length: int

        self.interface_symbols: Dict[str, str] = {'mid': '+', 
                                                  'line_a': '-', 
                                                  'line_b': '=', 
                                                  'div': '|'}
        
        

        self.update()


    def update(self) -> None:
        configs = self.app.configs

        self.contents_pos = configs.contents_pos
        self.headers_pos = configs.headers_pos

        self.min_interface_size = configs.min_interface_size
        self.max_string_length = configs.max_string_length

    















    def display_interface(
            self, 
            headers: List[str],
            contents: List[List[str]], 
            *, 
            use_last_col: Optional[bool] = True,
    ) -> None:

        headers_pos = self.headers_pos
        contents_pos = self.contents_pos

        # Create a List based on the size of 'len(headers)', Assigning integers representing lengths.
        # It can either distribute a value evenly or place a specific value at the end of the list
        distributed_str_sizes = evenly_assign_value_to_list(
                                    value=self.min_interface_size, 
                                    size=len(headers), 
                                    assign_at_end=use_last_col)


        # Calculate each 'str_size' based on 'max_content_length' and change 'distributed_str_sizes' if necessary.
        for i in range(len(headers)):
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
            # TODO: check if works
            if sum(distributed_str_sizes) >= self.min_interface_size:
                distributed_str_sizes[i] = match_parity(value=distributed_str_sizes[i], target_parity="even", decrease=True)
            else:
                distributed_str_sizes[i] = match_parity(value=distributed_str_sizes[i], target_parity="even", decrease=False)


        border_string, symbols_count = self.__build_border(
                                                headers_sizes=distributed_str_sizes,
                                                headers_qty=len(headers))


        headers_string = self.__build_headers(headers=headers, headers_pos=headers_pos, symbols_count=symbols_count)


        contents_string = self.__build_contents(contents=contents, contents_pos=contents_pos, symbols_count=symbols_count)


        print(border_string)
        print(headers_string)
        print(border_string)
        print(contents_string, end="")
        print(border_string)












    def __build_border(
            self, 
            *,
            headers_sizes: List[int], 
            headers_qty: Optional[int] = 1,
            symbols: Optional[Dict[str, str]] = None
        ) -> Tuple[str, List[int]]:

        symbols = symbols if symbols is not None else self.interface_symbols


        symbol_count: List[int] = []
        border: str = symbols['mid']

        for i in range(headers_qty): 

            for n in range(headers_sizes[i]): 

                if n % 2 == 0:
                    border += symbols['line_a']  # Add 'line_a' for even indices.

                else:
                    border += symbols['line_b']  # Add 'line_b' for odd indices.

                if headers_sizes[i] - 2 == n: 
                    border += symbols['mid']  # add 'mid' if it is the end of the column.
                    symbol_count.append(n)  
                    break

        return border, symbol_count
    

    def __build_headers(
            self,
            *,
            headers: List[str],
            headers_pos: List[str],
            symbols_count: List[int],
            div_symbol: Optional[str] = None
        ) -> str:

        div_symbol = div_symbol if div_symbol is not None else self.interface_symbols['div']


        built_headers: str = div_symbol # Default is '|'
        for i in range(len(headers)):
            
            pos = self.__get_pos(positions=headers_pos, index=i)

            visual_width = self.__get_visual_width(string=headers[i])

            width = symbols_count[i] - visual_width
            built_headers += self.__format_string(string=headers[i], width=width, pos=pos, div_symbol=div_symbol)


        return built_headers
    

    def __build_contents(
            self,
            *,
            contents: List[List[str]],
            contents_pos: List[str],
            symbols_count: List[int],
            div_symbol: Optional[str] = None
        ) -> str:

        div_symbol = div_symbol if div_symbol is not None else self.interface_symbols['div']


        built_contents: str = ""
        for i in range(len(contents)):
            built_contents += div_symbol # Default is '|'
            
            for y in range(len(symbols_count)):

                pos = self.__get_pos(positions=contents_pos, index=y)

                visual_width = self.__get_visual_width(string=contents[i][y])

                width = symbols_count[y] - visual_width
                built_contents += self.__format_string(
                                            string=contents[i][y],
                                            width=width,
                                            pos=pos,
                                            div_symbol=div_symbol)
                
            built_contents += "\n"

        
        return built_contents


    def __get_pos(
            self, 
            *, 
            positions: List[str],
            index: int
        ) -> str:

        try:
            pos = positions[index]
        except IndexError:
            pos = positions[-1]

        return pos


    def __get_visual_width(
            self, 
            *, 
            string: str
        ) -> int:

        visual_width: int = 0

        if has_non_ascii(string):
            visual_width = wcswidth(string) - len(string)
        else:
            visual_width = len(string)

        return visual_width


    def __format_string(
            self,
            *,
            string: str,
            width: int,
            pos: str,
            div_symbol: str,
            func: Optional[Callable[[str], str]] = None
        ) -> str:

        if func is not None:
            string = func(string)   

        if pos == 'left':  
            width -= 2 
            formated_string = f"   {string.ljust(width)}" + div_symbol

        elif pos == 'right':
            width -= 2 
            formated_string = f"{string.rjust(width)}   " + div_symbol

        else:  # Default is 'center'.
            width += 1 
            formated_string = f"{string.center(width)}" + div_symbol


        return formated_string






















    def display_msg_box(
            self, 
            *, 
            msg: str, 
            pos: Optional[str] = "right",
            div_symbol: Optional[str] = None,
            func: Optional[Callable[[str], str]] = None
        ) -> None:

        div_symbol = div_symbol if div_symbol is not None else self.interface_symbols['div']

        size = self.min_interface_size
        size = match_parity(value=size, target_parity="even", decrease=True)

        border, symbol_count = self.__build_border(headers_sizes=[size])

        # WTF IS THIS??? msg acts like a header!
        msg = self.__build_headers(headers=[msg], headers_pos=[pos], symbols_count=symbol_count, div_symbol=div_symbol)

        print(border)
        print(msg)




































    def select_from_display(
            self, 
            headers: List[Any], 
            contents: List[List[Any]], 
            *, 
            id: Optional[int] = 0,
        ) -> Any:

        while True:
            sleep(0.5)

            self.display_interface(
                headers=headers,
                contents=contents,
            )

            selection = read_int(msg=self.app.configs.input_msg)

            if selection == -1:  # Exception from 'read_int_input()'
                return selection # Return -1

            # Return a string based on the selected content and 'id'
            if len(contents) > (selection - 1) >= 0:  
                return str(contents[selection - 1][id])
            
            print("\nWarning - - -> Selection wasn't valid. Please, Try again.")
    












        