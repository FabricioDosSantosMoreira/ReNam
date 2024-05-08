from multiprocessing.pool import ThreadPool
import scandir
import shutil
import os


class DirectoryHandler():
    def __init__(self):

        self.excluded_paths: list[str] = ["C:/MinGW", "C:/CUE5", "C:/XboxGames", "C:/Intel"] # Only work when searching for a directory name, if an abspath is inserted it will not work.

        self.drives: list[str] = self.get_available_drives() 

        self.first_path_ocurrence: bool = False # If there are multiple directories with the same name do you want to stop searching when the first path is found? 
        self.absolute_path_found: bool = False # If an abspath path is found this will stop the search in other drives.

        # Renaming operations
        self.selected_directory_path: str = ""

        # Join operations 
        self.selected_out_folder_path: str = ""
        self.selected_join_paths: list[str] = [] 


    def get_all_directory_files(directory_path: str) -> list[str]:
        """"
        Retrieves all files within a specified directory.

        Args:
            directory_path (str): The path to the directory.

        Returns:
            list[str]: A list containing the names of all files within the directory.
        """
        
        print(f"\nSEARCHING ALL FILES WITHIN DIRECTORY [{directory_path}].")

        directory_files: list[str] = []

        for file_name in os.listdir(directory_path):

            file_path = os.path.join(directory_path, file_name)  # Construct full file path.
            if os.path.isfile(file_path):  # Check if the constructed path is a file.

                directory_files.append(file_name)  # Append the file name.

        print(f"\n{len(directory_files)} FILES WERE FOUND WITHIN DIRECTORY [{directory_path}].")
        return directory_files


    def set_selected_out_folder_path(self, path: str):
        """
        Sets the selected output folder path.

        Args:
            out_folder_path (str): The path to the output folder.
        """

        if os.path.isdir(path):
            self.selected_out_folder_path = path

            print(f"\nOUT FOLDER PATH WAS SET TO [{self.selected_out_folder_path}].")

        else:
            create_folder = str(input(f"\nPATH [{path}] WASN'T FOUND. DO YOU WANT TO CREATE A FOLDER INSTEAD? (Y/n) "))

            if create_folder.upper() == "Y":
                try:
                    os.makedirs(path, exist_ok=True)
                    self.selected_out_folder_path = path

                    print(f"\nFOLDER CREATED AT PATH [{self.selected_out_folder_path}].")

                except OSError:
                    print("\nERROR - - -> OCCURRED WHILE CREATING FOLDER.")

            else:
                print("\nERROR - - -> OUT FOLDER PATH WASN'T SET. KEEPING DEFAULT INSTEAD.")


    def set_selected_join_paths(self, paths: list[str]):
        """
        Set selected join paths from a list of paths.

        Args:
            paths (list[str]): List of paths to be selected.
        """

        for path in paths:

            if os.path.isdir(path):
                self.selected_join_paths.append(path)

            else:
                print(f"\nERROR - - -> THE PATH {path} DOESN'T EXISTS AND WILL NOT BE SELECTED.")


    def get_available_drives(self) -> list[str]:
        """
        Retrieves available drives in the system.

        Returns:
            list[str]: A list containing the paths of all available drives.
        """
        drives = []

        for drive in range(ord('A'), ord('Z') + 1):
            drive = chr(drive) + ':\\'
            if os.path.exists(drive):
                drives.append(drive)

        return drives

        
    def get_paths(self, directory: str) -> list[str]:
        """
        Retrieves paths matching the specified directory.

        Args:
            directory (str): The directory path to search.

        Returns:
            list[str]: A list containing the paths of directories matching the specified path.
        """

        self.absolute_path_found = False
        paths = []

        if not self.drives:
            print("\nERROR - - -> CAN'T CONTINUE WITHOUT DRIVES.")
        else:
            paths = self.search_drives(directory, self.drives)

        if paths:
            print(f"\nDIRECTORY [{directory}] WAS FOUND AT {paths}.")
        else:
            print(f"\nDIRECTORY {directory} WAS NOT FOUND.")
        
        return paths


    def search_drives(self, path: str, drives: list[str]) -> list[str]:
        """
        Searches for a path in multiple drives.

        Args:
            path (str): The path to search for.
            drives (list[str]): List of drive paths to search.

        Returns:
            list[str]: A list containing paths of the path found in any of the drives.
        """

        print(f"\nSEARCHING FOR DIRECTORY [{path}] IN MULTIPLE DRIVES {drives}.")

        results = []
        pool = ThreadPool(processes=19)

        for drive in drives:
            async_result = pool.apply_async(self.search_drive, args=(path, drive,))
            results.append(async_result)

        # Wait for all async results to finish.
        pool.close()
        pool.join()

        # Get the results from each async result and filter out None returns.
        results = [result.get() for result in results if result.get() is not None]
        # Flatten out the list of lists in results to a single list.
        flattened_results_list = [item for sublist in results for item in sublist]
    
        return flattened_results_list


    def search_drive(self, path:str, drive:str):
        """
        Searches for a path in a specific drive.

        Args:
            path (str): The path to search for.
            drive (str): The drive path to search in.

        Returns:
            list[str]: A list containing paths of the directory found in the specified drive.
        """
        print(f"\nSEARCHING FOR DIRECTORY [{path}] AT DRIVE [{drive}].")

        temp_paths = []

        temp_drive, sdp = os.path.splitdrive(path)
        temp_drive = f"{temp_drive}\\"  # Since [self.drives = chr(drive) + ':\\'], and [temp_drive = 'drive:'] we must insert a separator for consistency.

        if os.path.isabs(path) and temp_drive == drive and os.path.exists(path): # Verify if the path is an absolute path and if is in the same drive
            self.absolute_path_found = True
            return [path]

        else:
            for dirpath, dirnames, filenames in scandir.walk(drive):

                if not self.absolute_path_found and dirpath not in self.excluded_paths: # Check if an abspath was already found and if an path isn't in the excluded paths list.
                    if path in dirnames:
                        if self.first_path_ocurrence:
                            return [os.path.join(dirpath, path)]  
                        else:
                            temp_paths.append(os.path.join(dirpath, path))
                else: 
                    break
        
        return temp_paths






def join_folders(self) -> bool:
        

        # FAZER

        same_folders = False

        for _ in range(len(self.join_paths)):
            for __ in range(len(self.join_paths)):
                if self.join_paths[_] == self.join_paths[__] and not _ == __ :
                    same_folders = True


        # Is there any path? and are there at least 2 paths?
        if len(self.join_paths) >= 2 and not same_folders:

            # Is there an out folder path? If not, set to the first folder
            if not self.out_folder_path:
                self.set_out_folder_path(self.join_paths[0])


            for folder in range(len(self.join_paths), 0, -1):
                        
                files = os.listdir(folder)

                shutil.move()


            else:
                pass

        
        return False