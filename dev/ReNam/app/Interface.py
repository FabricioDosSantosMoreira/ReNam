from utils.generic_utils import categorize_contents
from utils.input_utils import read_str


class Interface():

    def __init__(self, app) -> None:
        from Main import Main

        self.app: Main = app


    def update(self) -> None:
        self.app.update()


    def quit(self) -> None:
        self.app.quit()
                

    def menu(self) -> None:
        while True:
            print("\n")

            self.app.interface_handler.display_msg_box(msg="ALOUUUUUUUUUUUU")

            HEADERS = ["OPTIONS", "MENU"]
            CONTENTS = categorize_contents(
                contents=["RENAM", "CONFIGS", "QUIT"]
            )
           
            option = self.app.interface_handler.display_and_select(HEADERS, CONTENTS)

            match int(option):
                case 1:
                    self.rename_menu()

                case 2:
                    self.configs_menu()

                case 3:
                    self.quit()


    def rename_menu(self) -> None:
        while True:
            print("\n")

            HEADERS = ["OPTIONS", "RENAME MENU"]
            CONTENTS = categorize_contents(
                contents=["SELECT DIRECTORY", "GO BACK", "QUIT"]
            )

            option = self.app.interface_handler.display_and_select(HEADERS, CONTENTS)

            match int(option):

                case 1: 
                    from pathlib import Path
                    _temp = read_str(msg="\nInsert full path or directory name: ")
                    if _temp == -1:
                        print("continue")
                        continue
                
                    try:
                        path = Path(_temp)
                        search = self.app.directory_handler.search_drives(path=path)
                        
                        str_search_list = []
                        for i in range(len(search)):
                            print(str(search[i]))
                            str_search_list.append(str(search[i]))

                        print(str_search_list, "\n\n\n")
                        if str_search_list:

                            HEADERS = ["OPTIONS", "PATHS"]
                            CONTENTS = categorize_contents(
                                contents=str_search_list
                            )

                        option = int(self.app.interface_handler.display_and_select(HEADERS, CONTENTS))

                        if option != -1:
                            dir = str_search_list[option - 1]

                            self.app.interface_handler.display_msg_box(msg = f"{dir}")


                    except Exception as e:
                        raise e
                        print(f"EXCEPTION {e}")


                    
                case 2:
                    self.menu()

                case 3:
                    self.quit()

        
        












    def configs_menu(self) -> None:
        print("\n")

        print(self.app.configs)

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


        self.app.interface_handler.display_interface(HEADERS, CONTENTS)

        self.menu()        
       


    






