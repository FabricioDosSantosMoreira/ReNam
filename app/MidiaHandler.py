from DirectoryHandler import DirectoryHandler
from LogHandler import generate_rename_log
import ApiHandler
import re
import os


class MidiaHandler():
    def __init__(self) -> None:

        self.midia_name: str = ""  # Tv/Movie name
        self.midia_season: int = 0  # The midia season, only for Tv
        self.start_from:int = 0 # Which episode number do you want to start renaming?

        self.file_format: list[str] = [".mp4", ".mkv", ".zip", ".srt", ".ssa", ".ass"] 
        self.selected_file_format:str = ""

        self.midia_type: list[str] = ["tv", "movie"] 
        self.selected_midia_type:str = ""
        
        self.patterns: list[str] = [r'S(\d+)E(\d+)', r's(\d+)\.e(\d+)', r'EP\.(\d+)\.'] 
        # r'S(\d+)E(\d+)' = expression pattern to capture episode number in the format "S01E20", 

        self.selected_pattern:str = ""


    def set_selected_pattern(self, pattern: str):
        self.selected_pattern = pattern
        print(f"\nSELECTED PATTERN WAS SET TO [{self.selected_pattern}].")


    def set_selected_file_format(self, file_format:str):
        self.selected_file_format = file_format
        print(f"\nSELECTED FILE FORMAT WAS SET TO [{self.selected_file_format}].")
 

    def set_selected_midia_type(self, midia_type:str):
        self.selected_midia_type = midia_type
        print(f"\nSELECTED MIDIA TYPE WAS SET TO [{self.selected_midia_type}].")

    
    def set_start_from(self, start_from:int) -> None:
        if start_from >= 1:
            self.start_from = start_from


    def set_midia_name(self, midia_name:str):
        self.midia_name = midia_name


    def set_midia_season(self, midia_season:int):
        self.midia_season = midia_season


    def extract_eps_order(self, files_names_names: list[str], pattern:str) -> dict[int, str]:

        file_order: dict[int, str] = {}
        filtered_items = {}

        for filename in files_names_names:
            match = re.search(pattern, filename)

            if match:
                try:
                    order = int(match.group(match.lastindex))
                    file_order[order] = filename

                except AttributeError:
                    print("\nERROR - - -> AtributeError.")
                except ValueError:
                    print("\nERROR - - -> ValueError.")

        if file_order:
            #for key, value in file_order.items():
                #if key >= self.start_from:
                    #filtered_items[key] = value

            #if filtered_items:
            filtered_items = dict(sorted(file_order.items()))


        return filtered_items 

    
    def filter_file_format(self, directory_files_names: list[str], file_format: str):
        # This function will filter the directory_files_names and return only selected_file_format files_names
        filtered_files_names = []

        for file in directory_files_names:
            if file.endswith(file_format):
                    filtered_files_names.append(file)
                    
        return filtered_files_names
 

    def rename(self, directory_path: str, midia_type:str) -> None:
        if midia_type == "tv":
            files_names = []
            # Get all files_names from the directory
            files_names = DirectoryHandler.get_all_directory_files(directory_path)
            files_names = self.filter_file_format(files_names, self.selected_file_format)
            files_names = self.extract_eps_order(files_names, self.selected_pattern)
            
        elif midia_type == "movie":
            # Get all files_names from the directory
            files:list[str] = []
            files = DirectoryHandler.get_all_directory_files(directory_path)
            files = self.filter_file_format(files, self.selected_file_format)

            files_names = {}
            for i, file in enumerate(files):
                files_names[i] = file

            if len(files_names.keys()) > 1:
                print("\nERROR - - -> MUST BE ONLY ONE MOVIE.")
                files_names.clear()


        print("\ndepois", files_names)
        if files_names:

            # Get all new names for midia name using the ApiHandler
            new_files_names = ApiHandler.get_midia_name(files_names, self.selected_midia_type, self.midia_name, self.midia_season, self.start_from)

            

            if not new_files_names == None and not files_names == None and len(files_names) > 0 and len(new_files_names) > 0:        
                # Remove any special caracter
                new_files_names = [re.sub(r'[<>:"/\\|?*]', '', name) for name in new_files_names]

                for i in range(len(new_files_names)):
                    new_files_names[i] =  new_files_names[i] + self.selected_file_format

                files_names_list = []
                    
                for key, value in files_names.items():
                    print(key, value)
                    files_names_list.append(value)


                print(files_names_list)
                print(new_files_names)
                 
                if len(files_names_list) == len(new_files_names):
                    
                    generate_rename_log(files_names_list, new_files_names, self.midia_name, self.midia_season, directory_path)
                    
                    rename = input("\nDO YOU WANT TO RENAME? (Y/n) ")
                    if  rename.lower() == "y":
                        print("\nRENAMING...")

                        for i, file in enumerate(files_names_list):
                            os.rename(os.path.join(directory_path, file), os.path.join(directory_path, f"{new_files_names[i]}"))
                    else:
                        print("\nRENAMING FILES CANCELED. LOG FILE WILL NOT BE EXCLUDED.")
                
                else:
                    generate_rename_log(files_names_list, new_files_names, self.midia_name, self.midia_season, directory_path)
                    print("\nERROR -> files_names and new_files_names DOESN'T HAVE THE SAME SIZE.")
            else:
                print("\nERROR - - -> API RETURNED NONE.")
        else:
            print(f"\nERROR - - -> NO FILES FOUND USING [{self.selected_pattern}].")