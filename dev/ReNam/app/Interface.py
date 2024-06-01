from utils.interface_utils import display_interface, interface_msg
from utils.any_utils import categorize_list
from handlers.ConfigsHandler import ConfigHandler

from typing import Optional
from utils.input_utils import read_str_input

class Interface():

    def __init__(self, app) -> None:
        self.app = app
        self.configs: ConfigHandler = app.configs


    def quit(self) -> None:
        self.app.is_running = False
        self.app.update()

    
    def display_select(self, headers, contents, id: Optional[int]) -> str:

        display_interface(
                headers=headers,
                contents=contents,
                headers_pos=self.configs.headers_pos,
                contents_pos=self.configs.contents_pos,
                main_header_id=self.configs.min_interface_size,
            )
        
        while True:
            selection = read_int_input(msg=input_msg)
            if selection == -1:  # Exception from 'read_int_input'
                return ''

            # Return a string based on the selected content and 'main_header_id'
            if len(contents) > (selection - 1) >= 0:  
                return str(contents[selection - 1][main_header_id])
            
            else:
                print("\nWarning - - -> Selection wasn't valid. Please, Try again.\n")








    def menu(self) -> None:
        while True:

            print("\n")

            CONTENTS = categorize_list(["RENAME FILES MENU", "QUIT"])
            HEADERS = ["OPTIONS", "MENU"]

            self.display_select(HEADERS, CONTENTS)

            
                









            match option:

                case 1:
                    self.rename_files_menu()
                case 2:
                    quit()

           
         

