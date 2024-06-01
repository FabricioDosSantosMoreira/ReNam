from utils.interface_utils import display_interface, interface_msg
from utils.any_utils import categorize_list
from handlers.ConfigsHandler import ConfigHandler

from typing import List, Any, Optional
from utils.input_utils import read_int_input


class Interface():

    def __init__(self, app) -> None:
        self.app = app
        self.configs: ConfigHandler = app.configs


    def quit(self) -> None:
        self.app.is_running = False
        self.app.update()

    
    def display_select(self, headers: List[Any], contents: List[List[Any]], id: Optional[int] = 0) -> str:

        print("\ndentyro: ", self.configs.min_interface_size)

        display_interface(
                headers=headers,
                contents=contents,
                headers_pos=self.configs.headers_pos,
                contents_pos=self.configs.contents_pos,
                min_interface_size=self.configs.min_interface_size,
            )
        
        while True:
            selection = read_int_input(msg=self.configs.input_msg)
            if selection == -1:  # Exception from 'read_int_input'
                return ''

            # Return a string based on the selected content and 'main_header_id'
            if len(contents) > (selection - 1) >= 0:  
                return str(contents[selection - 1][id])
            
            else:
                print("\nWarning - - -> Selection wasn't valid. Please, Try again.\n")


    def menu(self) -> None:
        while True:

            print("\n")

            CONTENTS = categorize_list([["RENAME漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字字漢字漢字漢字漢漢字漢字漢字 FILES MENU"], ["QUIT"]])
            HEADERS = ["OPTIONS", "ME漢字NU"]

            option = self.display_select(HEADERS, CONTENTS)

            match option:

                case '1':
                    print("a")
                    print("\n", self.configs.min_interface_size)
                case '2':
                    self.quit()

            
            a = input("here: ")

            if a == '1':
                self.configs.update()

                print("\n", self.configs.min_interface_size)

                self.menu()

           
         

