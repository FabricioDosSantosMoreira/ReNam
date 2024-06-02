from typing import Optional, Dict, List, Any


from utils.generic_utils import categorize_contents


class Interface():

    def __init__(self, app) -> None:
        from Main import Main

        self.app: Main = app


    def update(self) -> None:
        self.app.update()
                
        
    def menu(self) -> None:
        while True:
            print("\n")

            HEADERS = ["OPTIONS", "MENU"]
            CONTENTS = categorize_contents(["RENAM", "CONFIGS", "QUIT"])
           
            option = self.app.interface_handler.select_from_display(HEADERS, CONTENTS)

            match int(option):
                case 1:
                    self.rename_menu()

                case 2:
                    self.configs_menu()

                case 3:
                    self.app.quit()


    def configs_menu(self) -> None:
        print("\n")

        HEADERS = ["CONFIG", "VALUE"]
        CONTENTS = categorize_contents(
            contents=[
                str(self.app.configs.input_msg).strip("\n"),
                str(self.app.configs.min_interface_size), 
                str(self.app.configs.max_string_length),
                str(self.app.configs.string_delimiter),
                str(self.app.configs.headers_pos),
                str(self.app.configs.contents_pos),
            ], 
            identifiers=[
                "input_message",
                "min_interface_size", 
                "max_string_length",
                "sring_delimiter", 
                "headers_pos",
                "contents_pos",
            ]
        )

        print(HEADERS)
        print(CONTENTS)

        self.app.interface_handler.display_interface(HEADERS, CONTENTS)

        self.menu()        
       


    def rename_menu(self) -> None:
        pass






