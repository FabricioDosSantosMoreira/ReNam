from pathlib import Path
from app.classes.handlers.directory_handler import DirectoryHandler

from typing import List, Union

from app.core.exceptions import APIFetcherException
from app.classes.handlers.midia_handler import MidiaEnum, Movie, Series
from app.assets.utils.inputs import read_str

from app.assets.utils.generics import categorize_contents

from main import Main

def read_path(app: Main):

    temp_str = read_str(msg="\nInsert full path or directory name: ")
    if temp_str == -1: # Exception from 'read_str()', return None
        return None

    print(f"\n└─────────────> Please wait while ['{temp_str}'] is being searched...\n")
    search = app.directory_handler.search_drives(path=temp_str)

    # If 'search' doesn't contain a path
    if search is None:
        print(f"\n└─────────────> The directory path [{temp_str}] wasn't found.\n")
        return None
    
    # If 'search' only contains a single path
    if len(search) == 1:               
        return search[0]


    search_as_str = []
    for i in range(len(search)):
        search_as_str.append(str(search[i]))

    HEADERS = ["OPTIONS", "PATHS"]
    CONTENTS = categorize_contents(contents=search_as_str)

    option = app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
    if option == -1: # Exception from 'read_str()', return None
        return None
    
    return search[int(option) - 1]
    

def rename(app: Main) -> None:

    MIDIAS = MidiaEnum.list_all()

    HEADERS = ["OPTIONS", "MIDIA TYPE"]
    CONTENTS = categorize_contents(contents=MIDIAS)

    option = app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
    if option == -1: # Exception from 'read_str()', return None
        return None
    
    selected_midia = str(MIDIAS[int(option) - 1]).lower()


    title = read_str(msg=f"\n└─────────────> Insert a {selected_midia} title: ")
    if title == -1: # Exception from 'read_str()', return None
        return None


    if selected_midia == 'movie':
        MidiaInstance = MidiaEnum.MOVIE.get_instance(app)
        results = app.api_fetcher.fetch_movies(title=title)

    else:
        MidiaInstance = MidiaEnum.SERIES.get_instance(app)
        results = app.api_fetcher.fetch_series(title=title)

    if not results:
        print("\n└─────────────> TMDB API search didn't find anything.")
        return None


    HEADERS = ["OPTIONS", "TITLE", "RELEASE DATE", "ID"]
    CONTENTS = categorize_contents(contents=results)

    option = app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
    if option == -1: # Exception from 'read_str()', return None
        return None
    
    # 'results' = ['Content Id', 'Title', 'Release Date', 'TMDB Id']
    # 'results[1]' Refers to the title
    info: List[str] = results[int(option) - 1]
    title: str = str(results[int(option) - 1][1])
    # 'results[3]' Refers to the id
    id: int = int(results[int(option) - 1][3])

    MidiaInstance.title = title

    files = DirectoryHandler.get_directory_files(app.directory_handler.selected_path)
    if type(MidiaInstance) == Movie:
        MidiaInstance.rename(
            files=files,
            info=info
            )




    if type(MidiaInstance) == Series:

        seasons = app.api_fetcher.fetch_series_seasons(title=title, id=id)

        app.interface_handler.display_msg_box(msg=f"{title.title()} SEASONS")
        HEADERS = ["OPTIONS", "SEASON NUMBER", "SEASON NAME", "EPISODE COUNT"]
        CONTENTS = categorize_contents(contents=seasons)

        option = app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
        if option == -1: # Exception from 'read_str()', return None
            return None

        # 'seasons' = ['Interface ID', 'Season Number', 'Season Name', 'Episode Count', 'TMDB Season Id']
        season_number = str(seasons[int(option) - 1][1])

        episodes = app.api_fetcher.fetch_series_episodes(series_id=id, season_number=season_number)
        print(episodes)
        








        #ANIMES
        # # Seleciona o episode-group
        # groups = app.api_fetcher.fetch_series_episode_groups(series_id=id, title=title)

        # HEADERS = ["OPTIONS", "NAME", "EPISODE COUNT", "GROUP ID"]
        # CONTENTS = categorize_contents(contents=groups)

        # app.interface_handler.display_msg_box(msg="EPISODE GROUPS")
        # option = app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
        # if option == -1: # Exception from 'read_str()', return None
        #     return None
        
        # # 'groups' = ['Content Id', 'Name', 'Episode Count', 'TMDB Ep. Group Id']
        # group_id = str(groups[int(option) - 1][3])

        # seasons = app.api_fetcher.fetch_series_group(group_id=group_id, title=title)

        # #app.api_fetcher.fetch_seasons(series_id=id, seasons=seasons)
        

    print(MidiaInstance.title)
    print(MidiaInstance)


    


