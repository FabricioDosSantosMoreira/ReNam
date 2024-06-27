import time

from typing import List, Union

from app.core.exceptions import APIFetcherException
from app.classes.handlers.midia_handler import MidiaEnum, Movie, Series
from app.assets.utils.generic_utils import categorize_contents
from app.assets.utils.input_utils import read_str
from app.classes.handlers.directory_handler import DirectoryHandler


class Interface():

    def __init__(self, app) -> None:
        from main import Main
        
        self.app: 'Main' = app
        #self.welcome()

        
    def update(self) -> None:
        self.app.update()


    def quit(self) -> None:
        self.app.quit()
                

    def menu(self) -> None:
        while True:
            print("\n")

            HEADERS = ["OPTIONS", "MENU"]
            CONTENTS = categorize_contents(contents=["GO TO RENAM", "SHOW CONFIGS", "UPDATE CONFIGS", "QUIT"])
           
            option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
            match int(option):
                case 1:
                    self.rename_menu()

                    continue
                case 2:
                    self.configs_menu()

                    continue
                case 3:
                    self.update()

                    continue
                case 4:
                    self.quit()


    def rename_menu(self) -> None:
        while True:
            print("\n")

            if self.app.directory_handler.selected_path:
                self.app.interface_handler.display_msg_box(
                    msg=f"SELECTED DIRECTORY: {self.app.directory_handler.selected_path}",
                )
                files = self.app.directory_handler.get_directory_files(
                    path=self.app.directory_handler.selected_path
                )

                self.app.interface_handler.display_msg_box(
                    msg=f"{len(files)} FILES FOUND"
                )

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

                    if not self.app.directory_handler.selected_path:
                        print("Please select a path first")

                    else:
                        self.rename()

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
        

    def rename(self) -> None:

        MIDIAS = MidiaEnum.list_all()

        HEADERS = ["OPTIONS", "MIDIA TYPE"]
        CONTENTS = categorize_contents(contents=MIDIAS)

        option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
        if option == -1: # Exception from 'read_str()', return None
            return None
        
        selected_midia = str(MIDIAS[int(option) - 1]).lower()


        title = read_str(msg=f"\n└─────────────> Insert a {selected_midia} title: ")
        if title == -1: # Exception from 'read_str()', return None
            return None


        if selected_midia == 'movie':
            MidiaInstance = MidiaEnum.MOVIE.get_instance(self.app)
            results = self.app.api_fetcher.fetch_movies(title=title)

        else:
            MidiaInstance = MidiaEnum.SERIES.get_instance(self.app)
            results = self.app.api_fetcher.fetch_series(title=title)

        if not results:
            print("\n└─────────────> TMDB API search didn't find anything.")
            return None


        HEADERS = ["OPTIONS", "TITLE", "RELEASE DATE", "ID"]
        CONTENTS = categorize_contents(contents=results)

        option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
        if option == -1: # Exception from 'read_str()', return None
            return None
        
        # 'results' = ['Content Id', 'Title', 'Release Date', 'TMDB Id']
        # 'results[1]' Refers to the title
        info: List[str] = results[int(option) - 1]
        title: str = str(results[int(option) - 1][1])
        # 'results[3]' Refers to the id
        id: int = int(results[int(option) - 1][3])

        MidiaInstance.title = title

        files = DirectoryHandler.get_directory_files(self.app.directory_handler.selected_path)
        if type(MidiaInstance) == Movie:
            MidiaInstance.rename(
                files=files,
                info=info
                )




        if type(MidiaInstance) == Series:

            seasons = self.app.api_fetcher.fetch_series_seasons(title=title, id=id)

            self.app.interface_handler.display_msg_box(msg=f"{title.title()} SEASONS")
            HEADERS = ["OPTIONS", "SEASON NUMBER", "SEASON NAME", "EPISODE COUNT"]
            CONTENTS = categorize_contents(contents=seasons)

            option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
            if option == -1: # Exception from 'read_str()', return None
                return None

            # 'seasons' = ['Interface ID', 'Season Number', 'Season Name', 'Episode Count', 'TMDB Season Id']
            season_number = str(seasons[int(option) - 1][1])

            episodes = self.app.api_fetcher.fetch_series_episodes(series_id=id, season_number=season_number)
            print(episodes)
            








            #ANIMES
            # # Seleciona o episode-group
            # groups = self.app.api_fetcher.fetch_series_episode_groups(series_id=id, title=title)

            # HEADERS = ["OPTIONS", "NAME", "EPISODE COUNT", "GROUP ID"]
            # CONTENTS = categorize_contents(contents=groups)

            # self.app.interface_handler.display_msg_box(msg="EPISODE GROUPS")
            # option = self.app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
            # if option == -1: # Exception from 'read_str()', return None
            #     return None
            
            # # 'groups' = ['Content Id', 'Name', 'Episode Count', 'TMDB Ep. Group Id']
            # group_id = str(groups[int(option) - 1][3])

            # seasons = self.app.api_fetcher.fetch_series_group(group_id=group_id, title=title)

            # #self.app.api_fetcher.fetch_seasons(series_id=id, seasons=seasons)
            

        print(MidiaInstance.title)
        print(MidiaInstance)


    



















    def configs_menu(self) -> None:
        print("\n")


        print(list(self.app.configs.configs.values()))


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


    def welcome(self) -> None:
        message: str = self.app.configs.welcome

        for line in message:
            print(line, end='')

        time.sleep(1.50)
       


    





