from typing import Callable, Optional, Tuple, Dict, List, Any
from wcwidth import wcswidth
import time

from app.assets.utils.generics import match_parity, evenly_assign_value_to_list
from app.assets.utils.strings import has_non_ascii, reduce_string_length, reduce_strings_length
from app.assets.utils.inputs import read_int


class InterfaceHandler():

    def __init__(self, app) -> None:
        from main import Main

        self.app: Main = app
    
        self.min_interface_size: int = 0
        self.max_string_length: int = 0

        self.interface_symbols: Dict[str, str] = {}
        self.delimiter: str = ''
        self.input_msg: str = ''

        self.headers_pos: List[str] = []
        self.contents_pos: List[str] = []
        self.headers_func: Callable[[str], str] = None
        self.contents_func: Callable[[str], str] = None

    
        self.update()


    def update(self) -> None:
        configs = self.app.config_handler

        self.min_interface_size = configs.min_interface_size
        self.max_string_length = configs.max_string_length

        self.interface_symbols = configs.interface_symbols
        self.delimiter = configs.delimiter
        self.input_msg = configs.input_msg

        self.headers_pos = configs.headers_pos
        self.contents_pos = configs.contents_pos
        self.headers_func = configs.headers_func
        self.contents_func = configs.contents_func


    def display_msg_box(
            self, 
            *,
            msg: str, 
            pos: Optional[str] = "left",
            border_at_end: Optional[bool] = False,
            func: Optional[Callable[[str], str]] = None
        ) -> None:

        msg = reduce_string_length(string=msg, length=self.max_string_length, delimiter=self.delimiter)

        # 'interface_size' must always be even
        interface_size = match_parity(value=self.min_interface_size, target_parity="even", decrease=True)

        # build 'border' and get the 'width_count' used to build
        border, width_count = self.__build_border(
                                        column_widths=[interface_size], 
                                        num_of_columns=1, 
                                        symbols=self.interface_symbols
                                    )

        # 'msg' acts like a header
        msg = self.__build_headers(
                        headers=[msg], 
                        headers_pos=[pos], 
                        width_count=width_count, 
                        symbols=self.interface_symbols,
                        func=func
        )


        print(border)
        print(msg)
        if border_at_end is True:
            print(border)


    def display_and_select(
            self, 
            *,
            headers: List[str], 
            contents: List[List[str]], 
            index: Optional[int] = 0,
        ) -> str:

        while True:
            time.sleep(0.75)

            self.display_interface(headers=headers.copy(),contents=contents.copy())

            selection = read_int(msg=self.input_msg)
            if selection == -1:  # Exception from 'read_int()', return -1.
                return -1

            # Return a string based on the selected content and its 'index'.
            if len(contents) > (selection - 1) >= 0:  
                return str(contents[selection - 1][index])
            
            print("\nWarning - - -> Selection wasn't valid. Please, Try again.")
                

    def display_interface(
            self, 
            *,
            headers: List[str],
            contents: List[List[str]], 
            use_last_col: Optional[bool] = True,
    ) -> None:
        
        headers = reduce_strings_length(
                    strings=headers, 
                    length=self.max_string_length, 
                    delimiter=self.delimiter, 
                )
        
        for i, content in enumerate(contents):
            contents[i] = reduce_strings_length(
                            strings=content, 
                            length=self.max_string_length, 
                            delimiter=self.delimiter, 
                            end_cut=True # False
                        )

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
            # TODO: check which works
            # max_content_length = max(wcswidth(content[i]) for content in contents)
            max_content_length = max(self.__get_visual_width(string=content[i]) for content in contents)
            header_length = self.__get_visual_width(string=headers[i]) 


            # Add the largest value to 'str_size'.
            if max_content_length > header_length:
                str_size += max_content_length
            else:
                str_size += header_length 

            # If the value calculated in 'assign_distributed_list' isn't enough, change to 'str_size'.
            if distributed_str_sizes[i] < str_size:
                distributed_str_sizes[i] = str_size


        # Calculate the necessary size for the last column
        if use_last_col:
            sizes_sum = sum(distributed_str_sizes) - distributed_str_sizes[-1]
            if distributed_str_sizes[-1] > max_content_length:
                distributed_str_sizes[-1] -= sizes_sum

            if distributed_str_sizes[-1] < max_content_length + len(headers[-1]):
                distributed_str_sizes[-1] = max_content_length + len(headers[-1]) + 1 


        # Adjust the sizes in 'distributed_str_sizes' to ensure only even sizes, decreases by '1' if odd.
        for i in range(len(distributed_str_sizes)):
            # TODO: check if works
            if sum(distributed_str_sizes) >= self.min_interface_size:
                distributed_str_sizes[i] = match_parity(value=distributed_str_sizes[i], target_parity="even", decrease=True)
            else:
                distributed_str_sizes[i] = match_parity(value=distributed_str_sizes[i], target_parity="even", decrease=False)


        border_string, width_count = self.__build_border(
                                                column_widths=distributed_str_sizes,
                                                num_of_columns=len(headers),
                                                symbols=self.interface_symbols)

        headers_string = self.__build_headers(
                                    headers=headers, 
                                    headers_pos=self.headers_pos, 
                                    width_count=width_count, 
                                    symbols=self.interface_symbols,
                                    func=self.headers_func
                                )

        contents_string = self.__build_contents(
                                    contents=contents, 
                                    contents_pos=self.contents_pos, 
                                    width_count=width_count, 
                                    symbols=self.interface_symbols,
                                    func=self.contents_func
                                )


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


        return border, width_count
    

    def __build_headers(
            self,
            *,
            headers: List[str],
            headers_pos: List[str],
            width_count: List[int],
            symbols: Dict[str, str],
            func: Optional[Callable[[str], str]] = None
        ) -> str:

        
        built_headers = symbols['div']  # Start with the 'div' symbol
        for i, header in enumerate(headers):
            
            alignment = self.__get_alignment(alignments=headers_pos, index=i)

            # FIXME: WTFF!????
            visual_width = self.__get_visual_width(string=header)
            a = 0
            if not visual_width == len(header):
                a = wcswidth(header) - len(header)

            width = width_count[i] - a #- visual_width

            built_headers += self.__format_string(
                                        string=header, 
                                        width=width, 
                                        alignment=alignment, 
                                        divider=symbols['div'],
                                        func=func,
                                    )


        return built_headers
    

    def __build_contents(
            self,
            *,
            contents: List[List[str]],
            contents_pos: List[str],
            width_count: List[int],
            symbols: Dict[str, str],
            func: Optional[Callable[[str], str]] = None
        ) -> str:


        built_contents = ""  # Start with an empty string
        for i, content in enumerate(contents):
            built_contents += symbols['div'] 
            
            for w, string in enumerate(content):

                alignment = self.__get_alignment(alignments=contents_pos, index=w)

                # FIXME: WTFF!????
                visual_width = self.__get_visual_width(string=string)
                a = 0
                if not visual_width == len(string):
                    a = wcswidth(string) - len(string)
                    
                width = width_count[w] - a #- visual_width

                built_contents += self.__format_string(
                                            string=string,
                                            width=width,
                                            alignment=alignment,
                                            divider=symbols['div'],
                                            func=func
                                        )
                
            built_contents += "\n"

        
        return built_contents


    def __get_alignment(self, *, alignments: List[str], index: int) -> str:
        """
        Retrieve the alignment at the specified index from the list of alignments.
        If the specified index is out of range, return the last alignment in the list.
    
        Args:
        alignments (List[str]): A list of alignments strings.
        index (int): The index of the desired alignment in the list.
        
        Returns:
            str: 
                The alignment string at the specified index or the last alignment if the index is out of range.
        """

        try:
            # Attempt to retrieve the alignment at the specified index.
            pos = alignments[index]  
        except IndexError:
            # If the index is out of range, return the last alignment in the list.
            pos = alignments[-1]


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

        # Check if the string contains any non-ASCII characters.
        non_ascii, i = has_non_ascii(string)
        if non_ascii:
            # Calculate visual width using wcswidth and adjust for the length difference.
            visual_width = wcswidth(string) 
        else:
            # For ASCII strings, the visual width is simply the length of the string.
            visual_width = len(string)


        return visual_width


    def __format_string(
            self,
            *,
            string: str,
            width: int,
            alignment: str,
            divider: str,
            func: Optional[Callable[[str], str]] = None
        ) -> str:
        """
        Formats a given string according to specified alignment, width, and a divider.

        Parameters:
            string (str): The string to be formatted.
            width (int): The width to which the string should be aligned.
            alignment (str): The position for alignment.
            divider (str): A divider string appended to the formatted string.
            func (Optional[Callable[[str], str]]): A function to apply to the string before formatting. Defaults to None.

        Returns:
            str: 
                The formatted string with the specified alignment, width, and divider.
        """

        # Apply a function to the string
        if func is not None:
            string = func(string)   


        # Check the alignment position
        if alignment == 'center':  
            width += 1  # Adjust width for centering
            formated_string = f"{string.center(width)}" + divider

        elif alignment == 'right':
            width -= 2  # Adjust width for right-justifying
            formated_string = f"{string.rjust(width)}   " + divider

        else:  # Default alignment is 'left'
            width -= 2  # Adjust width for left-justifying
            formated_string = f"   {string.ljust(width)}" + divider


        return formated_string
    