import time

from utils.generic_utils import categorize_contents
from utils.input_utils import read_str


class Interface():

    def __init__(self, app) -> None:
        from Main import Main

        self.app: Main = app

        # for _ in self.app.configs.welcome:
        #     print(_, end='')
        # time.sleep(2.50)
        # print("\n\n\n")


    def update(self) -> None:
        self.app.update()


    def quit(self) -> None:
        self.app.quit()
                

    def menu(self) -> None:
        while True:
            print("\n")

            HEADERS = ["OPTIONS", "MENU"]
            CONTENTS = categorize_contents(contents=["RENAME", "CONFIGS", "QUIT"])
           
            option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)

            match int(option):
                case 1:
                    self.rename_menu()

                    continue
                case 2:
                    self.configs_menu()

                    continue
                case 3:
                    self.quit()


    def rename_menu(self) -> None:
        while True:
            print("\n")

            HEADERS = ["OPTIONS", "RENAME MENU"]
            CONTENTS = categorize_contents(contents=["SELECT DIRECTORY", "RENAME", "GO BACK", "QUIT"])

            option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)

            match int(option):
                case 1: 
                    dir = self.read_path()

                    if dir:
                        self.app.directory_handler.selected_path = dir
                        print(f"\n└─────────────> Selected [{dir}] as directory.\n")

                    continue           
                case 2:
                    self.readings()
                    
                    continue
                case 3:
                    self.menu()

                case 4:
                    self.quit()

        
    def read_path(self):

        _temp = read_str(msg="\nInsert full path or directory name: ")
        if _temp == -1: # Exception from 'read_str()', return None
            return None

        print(f"\n└─────────────> Please wait while ['{_temp}'] is being searched...\n")
        search = self.app.directory_handler.search_drives(path=_temp)

        # If 'search' doesn't contain a path
        if search is None:
            print(f"\n└─────────────> The directory path [{_temp}] wasn't found.\n")
            return None
        
        # If 'search' only contains a single path
        if len(search) == 1:               
            return search[0]


        search_as_str = []
        for i in range(len(search)):
            search_as_str.append(str(search[i]))

        HEADERS = ["OPTIONS", "PATHS"]
        CONTENTS = categorize_contents(contents=search_as_str)

        option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
        if option == -1: # Exception from 'read_str()', return None
            return None
        
        return search[int(option) - 1]
        

    def readings(self) -> None:

        a = []
        midias = self.app.midia_handler.list_all()
        print(midias)
        










    def configs_menu(self) -> None:
        print("\n")

        print(self.app.configs)

        HEADERS = ["CONFIG", "VALUE"]
        CONTENTS = categorize_contents(
            contents=[
                str(self.app.configs.input_msg).strip("\n"),
                str(self.app.configs.min_interface_size), 
                str(self.app.configs.max_string_length),
                str(self.app.configs.delimiter),
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


        self.app.interface_handler.display_interface(headers=HEADERS, contents=CONTENTS)

        self.menu()        
       


    





