import time

from app.assets.utils.generics import categorize_contents


class Interface():

    def __init__(self, app) -> None:
        from main import Main
        
        self.app: Main = app
        #self.welcome()

        
    def update(self) -> None:
        self.app.update()


    def quit(self) -> None:
        self.app.quit()
                

    def menu(self) -> None:
        while True:
            print("\n", end='')

            HEADERS = ["OPTIONS", "MENU"]
            CONTENTS = categorize_contents(contents=["RENAME", "UPDATE", "QUIT"])
           
            option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
            match int(option):
                case 1:
                    self.rename_menu()

                    continue
                case 2:
                    self.update()

                    continue
                case 3:
                    self.quit()


    def rename_menu(self) -> None:
        from app.core import logic

        while True:
            print("\n", end='')

            self.show_dir_info()
            
            HEADERS = ["OPTIONS", "RENAME MENU"]
            CONTENTS = categorize_contents(contents=["SELECT DIRECTORY", "RENAME FILES", "GO BACK", "QUIT"])

            option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
            match int(option):
                case 1: 
                    path = logic.select_path(app=self.app)  
                    if path:
                        self.app.directory_handler.selected_path = path
                        print(f"\n└─────────────> Selected [{path}] as directory.\n")

                    continue           
                case 2:
                    # TODO
                    # selected_path = self.app.directory_handler.selected_path
                    # if not selected_path:
                    #     print(f"\n└─────────────> Please select a directory first.\n")
                    #     continue

                    logic.rename(app=self.app)

                    continue
                case 3:
                    self.menu()

                case 4:
                    self.quit()

    
    def show_dir_info(self) -> None:
        path = self.app.directory_handler.selected_path

        if path:
            files = self.app.directory_handler.get_directory_files(path=path)

            self.app.interface_handler.display_msg_box(
                msg=f"SELECTED DIRECTORY: {path}",
            )

            if files:
                self.app.interface_handler.display_msg_box(
                    msg=f"{len(files)} FILES FOUND"
                )
        

    def welcome(self) -> None:
        message: str = self.app.config_handler.welcome

        for line in message:
            print(line, end='')

        time.sleep(1.50)
       