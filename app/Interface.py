from DirectoryHandler import DirectoryHandler
from MidiaHandler import MidiaHandler


class Interface():
    def __init__(self) -> None:
        pass


    def select_option(self, msg:str) -> int:
        while True:
            try:
                option = int(input(f"\n{msg}"))
                return option
            except ValueError:
                print("\nERROR - - -> INVALID OPTION. PLEASE, TRY AGAIN.")


    def select_from_list(self, list: list[str], selection_header: str) -> str:

        if len(list) == 1:
            return(list[0])
        
        else:
            selection_header = selection_header.upper()
            print("\n+-=-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
            print(f"|   SELECTION   |         {selection_header}", "|".rjust(106 - len(selection_header))                                                                                           )
            print("+-=-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
            
            for i, object in enumerate(list):
                print(f"|       {i + 1}       |         {object.upper()}", "|".rjust(106 - len(object)))
            print("+-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")

            while True:
                selection = self.select_option(f"- - - - - - -> PLEASE SELECT {selection_header} TO CONTINUE: ") - 1

                if len(list) > selection >= 0:
                    return(list[selection])
                else:
                    print("\nERROR - - -> SELECTION WASN'T VALID. PLEASE, TRY AGAIN.")  
        

    def menu(self) -> None:
        while True:
            print("\n+-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
            print("|   OPTIONS   |         ACTIONS                                                                                                     |")
            print("+-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
            print("|      1      |         RENAME FILES MENU                                                                                           |")
            print("|      2      |         QUIT                                                                                                        |")
            print("+-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
            
            match self.select_option("- - - - - - -> INSERT AN OPTION: "):
                case 1:
                    self.rename_files_menu()
                case 2:
                    quit()
                case _:
                    print("\nERROR - - -> SELECTED OPTION DOESN'T EXISTS. PLEASE, TRY AGAIN.")


    def rename_files_menu(self):

        self.Directory_handler = DirectoryHandler()
        self.Midia_handler = MidiaHandler()
        
        while True:
            

            selected_dir_path = self.Directory_handler.selected_directory_path

            if selected_dir_path:
                print("\n+-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
                print(f"| SELECTED DIRECTORY: {selected_dir_path}", "|".rjust(110 - len(selected_dir_path)))
                print("+-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
            else:
                print("\n+-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
            
            print("|   OPTIONS   |         RENAME MENU                                                                                                 |") 
            print("+-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
            print("|      1      |         SELECT DIRECTORY                                                                                            |")
            print("|      2      |         RENAME FILES                                                                                                |")  
            print("|      3      |         MAIN MENU                                                                                                   |")
            print("+-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
           
            match self.select_option("- - - - - - -> INSERT AN OPTION: "):
                case 1:

                    try:
                        directory = str(input("\n- - - - - - -> INSERT A DIRECTORY PATH OR NAME TO CONTINUE: "))
                    except ValueError:
                        print("\nERROR - - -> ValueError") 

                    paths = self.Directory_handler.get_paths(directory)

                    if paths:  # If paths isn't empty
                        self.Directory_handler.selected_directory_path = self.select_from_list(paths, "DIRECTORY PATH")

                        print(f"\nSELECTED [{self.Directory_handler.selected_directory_path}] AS DIRECTORY")     

                    else: 
                        print(f"\nERROR - - -> DIRECTORY PATH [{directory}] WASN'T FOUND.")

                    continue
                case 2:

                    if selected_dir_path: # If selected_dir_path isn't empty
                        
                        self.Midia_handler.set_selected_midia_type(self.select_from_list(self.Midia_handler.midia_type, "MIDIA TYPE"))

                        if self.Midia_handler.selected_midia_type == "tv":
                            while True:
                                try:
                                    midia_name = str(input("\n- - - - - - -> INSERT THE MIDIA NAME: "))
                                    self.Midia_handler.set_midia_name(midia_name)

                                    midia_season = int(input(f"\n- - - - - - -> INSERT THE SEASON FOR [{midia_name.upper()}]: "))
                                    self.Midia_handler.set_midia_season(midia_season)

                                    start_from = int(input("\n - - - - - - -> INSERT FROM WHICH EPISODE NUMBER START RENAMING: "))
                                    self.Midia_handler.set_start_from(start_from)

                                    break
                                except ValueError:
                                    print("\nERROR - - -> ValueError. PLEASE, TRY AGAIN.") 

                            self.Midia_handler.set_selected_file_format(self.select_from_list(self.Midia_handler.file_format, "FILE FORMAT"))
                            self.Midia_handler.set_selected_pattern(self.select_from_list(self.Midia_handler.patterns, "PATTERN"))

                            self.Midia_handler.rename(self.Directory_handler.selected_directory_path, "tv")

                        elif self.Midia_handler.selected_midia_type == "movie":
                            while True:
                                try:
                                    midia_name = str(input("\n- - - - - - -> INSERT THE MIDIA NAME: "))
                                    self.Midia_handler.set_midia_name(midia_name)

                                    break
                                except ValueError:
                                    print("\nERROR - - -> ValueError. PLEASE, TRY AGAIN.") 

                            self.Midia_handler.set_selected_file_format(self.select_from_list(self.Midia_handler.file_format, "FILE FORMAT"))
                            self.Midia_handler.rename(self.Directory_handler.selected_directory_path, "movie")
                
                    continue
                case 3:
                    self.menu()
                case _:
                    print("\nERROR - - -> SELECTED OPTION DOESN'T EXISTS. PLEASE, TRY AGAIN.")