from typing import List, Any, Optional
from time import sleep

from utils.interface_utils import display_interface, interface_msg
from utils.any_utils import categorize_list
from utils.input_utils import read_int_input


class Interface():

    def __init__(self, app) -> None:
        from Main import Main

        self.app: Main = app


    def __str__(self) -> str:
        raise NotImplementedError
        
        
    def menu(self) -> None:
        while True:
            print("\n")

            CONTENTS = categorize_list([["RENAME FILES"], ["QUIT"]])
            HEADERS = ["OPTIONS", "MENU"]

            option = self.select_from_display(HEADERS, CONTENTS)
            match int(option):

                case 1:
                    self.rename_menu()

                case 2:
                    self.app.quit()


    def rename_menu(self) -> None:
        pass


    def select_from_display(
            self, 
            headers: List[Any], 
            contents: List[List[Any]], 
            *, 
            id: Optional[int] = 0,
        ) -> Any:

        while True:
            sleep(1)

            display_interface(
                headers=headers,
                contents=contents,
                headers_pos=self.app.configs.headers_pos,
                contents_pos=self.app.configs.contents_pos,
                min_size=self.app.configs.min_interface_size,
            )

            selection = read_int_input(msg=self.app.configs.input_msg)

            if selection == -1:  # Exception from 'read_int_input()'
                return selection # Return -1

            # Return a string based on the selected content and 'id'
            if len(contents) > (selection - 1) >= 0:  
                return str(contents[selection - 1][id])
            
            print("\nWarning - - -> Selection wasn't valid. Please, Try again.")
