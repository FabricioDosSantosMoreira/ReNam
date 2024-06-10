from typing import Callable, Optional, Tuple, Dict, List, Any
from wcwidth import wcswidth
import time

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

        self.interface_symbols: Dict[str, str] = {'mid': '+', 'line_a': '-', 'line_b': '=', 'div': '|'}
        
        self.update()


    def update(self) -> None:
        configs = self.app.configs

        self.contents_pos = configs.contents_pos
        self.headers_pos = configs.headers_pos

        self.min_interface_size = configs.min_interface_size
        self.max_string_length = configs.max_string_length

        self.headers_func = str.title
        self.contents_func = str.lower

    
    def display_msg_box(
            self, 
            *,
            msg: str, 
            pos: Optional[str] = "left",
            border_at_end: Optional[bool] = False,
            func: Optional[Callable[[str], str]] = None
        ) -> None:

        # 'interface_size' must always be even
        interface_size = match_parity(value=self.min_interface_size, target_parity="even", decrease=True)

        # build 'border' and get the 'symbols_count' used to build
        border, symbol_count = self.__build_border(column_widths=[interface_size], num_of_columns=1, symbols=self.interface_symbols)

        # 'msg' acts like a header
        msg = self.__build_headers(
                        headers=[msg], 
                        headers_pos=[pos], 
                        symbols_count=symbol_count, 
                    )


        print(border)
        print(msg)
        if border_at_end is True:
            print(border)


    def display_and_select(
            self, 
            headers: List[str], 
            contents: List[List[str]], 
            *, 
            index: Optional[int] = 0,
        ) -> str:

        while True:
            time.sleep(0.75)

            self.display_interface(headers=headers,contents=contents)

            selection = read_int(msg=self.app.configs.input_msg)
            if selection == -1:  # Exception from 'read_int()', return -1.
                return -1

            # Return a string based on the selected content and its 'index'.
            if len(contents) > (selection - 1) >= 0:  
                return str(contents[selection - 1][index])
            
            print("\nWarning - - -> Selection wasn't valid. Please, Try again.")
                

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
                                                column_widths=distributed_str_sizes,
                                                num_of_columns=len(headers),
                                                symbols=self.interface_symbols)


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
            column_widths: List[int], 
            num_of_columns: int,
            symbols: Dict[str, str]
            
        ) -> Tuple[str, List[int]]:
        """
        Constructs a border string and a list of width counts.

        Args:


        Returns:
            Tuple[str, List[int]]: A tuple containing the border string and a list of width counts.
        """
        width_count: List[int] = []


        border = symbols['mid']  # Start with the 'mid' symbol
        for col in range(num_of_columns): 
            for width in range(column_widths[col] -1): 

                if width % 2 == 0:
                    border += symbols['line_a']  # Add 'line_a' symbol for even indices
                else:
                    border += symbols['line_b']  # Add 'line_b' symbol for odd indices

            border += symbols['mid']  # add 'mid' symbol to the end of the column
            width_count.append(width)

                # if column_widths[col] - 2 == width: 
                #      border += symbols['mid']  # add 'mid' if it is the end of the column
                #      width_count.append(width)  
                #      break


        return border, width_count
    






    def __build_headers(
            self,
            *,
            headers: List[str],
            headers_pos: List[str],
            symbols_count: List[int],
        ) -> str:

        div_symbol = self.interface_symbols['div']


        built_headers = div_symbol 
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
        ) -> str:

        div_symbol = self.interface_symbols['div']


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


    def __get_pos(self, *, positions: List[str], index: int) -> str:
        """
        Retrieve the position at the specified index from the list of positions.
        If the specified index is out of range, return the last position in the list.
    
        Args:
        positions (List[str]): A list of position strings.
        index (int): The index of the desired position in the list.
        
        Returns:
            str: 
                The position string at the specified index or the last position if the index is out of range.
        """
        pos: str

        try:
            # Attempt to retrieve the position at the specified index.
            pos = positions[index]  
        except IndexError:
            # If the index is out of range, return the last position in the list.
            pos = positions[-1]


        return pos


    def __get_visual_width(self, *, string: str) -> int:
        """
        Calculate the visual width of a given string.

        This function determines the visual width of a string, accounting for the 
        differences between ASCII and non-ASCII characters. Non-ASCII characters 
        may have different widths when displayed compared to ASCII characters.

        Args:
        string (str): The input string for which to calculate the visual width.

        Returns:
            int:
                The calculated visual width of the string.
        """
        visual_width: int

        # Check if the string contains any non-ASCII characters.
        if has_non_ascii(string):

            # Calculate visual width using wcswidth and adjust for the length difference.
            visual_width = wcswidth(string) - len(string)
        else:
            # For ASCII strings, the visual width is simply the length of the string.
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



        # Apply a function to the string, like title(), upper(), etc
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
