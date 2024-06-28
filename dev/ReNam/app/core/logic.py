from pathlib import Path
from app.classes.handlers.interface_handler import InterfaceHandler
from app.classes.handlers.directory_handler import DirectoryHandler
from typing import List, Union
from app.core.exceptions import APIFetcherException
from app.classes.handlers.midia_handler import Anime, MidiaEnum, Movie, Series
from app.assets.utils.inputs import read_str
from app.assets.utils.generics import categorize_contents
from main import Main


def read_path(app: Main) -> Union[List[Path], None]:

    value = read_str(msg="\nInsert full path or directory name: ")
    if value == -1: # Exception from 'read_str()', return None
        return None
    
    try:
        temp_path: Path = Path(value)
    except Exception as exc:
        print(f"\n└─────────────> Couldn't get a Path object out of ['{value}']\n")
        return None
    

    print(f"\n└─────────────> Please wait while ['{temp_path}'] is being searched...\n")
    search = app.directory_handler.search_drives(path=temp_path)
    if search is None:
        print(f"\n└─────────────> The directory path [{temp_path}] wasn't found.\n")
        return None
    

    return search
    

def select_path(app: Main, paths: List[Path]) -> Union[Path, None]:
    interface: InterfaceHandler = app.interface_handler

    # If 'paths' contains a single path
    if len(paths) == 1:               
        return paths[0]


    paths_as_str: List[str] = []
    for i in range(len(paths)):
        paths_as_str.append(str(paths[i]))


    HEADERS = ["OPTIONS", "PATHS"]
    CONTENTS = categorize_contents(contents=paths_as_str)

    option = interface.display_and_select(headers=HEADERS, contents=CONTENTS)
    if option == -1: # Exception from 'read_str()', return None
        return None

    return paths[int(option) - 1]
    

def rename(app: Main) -> None:
    interface: InterfaceHandler = app.interface_handler

    MIDIAS = MidiaEnum.list_all()
    HEADERS = ["OPTIONS", "MIDIA TYPE"]
    CONTENTS = categorize_contents(contents=MIDIAS)

    option = interface.display_and_select(headers=HEADERS, contents=CONTENTS)
    if option == -1: # Exception from 'read_str()', return None
        return None
    

    selected_midia = str(MIDIAS[int(option) - 1]).lower()

    value = read_str(msg=f"\n└─────────────> Insert a {selected_midia} title: ")
    if value == -1: # Exception from 'read_str()', return None
        return None
    else:
        title = value


    if selected_midia == 'movie':
        MidiaInstance = MidiaEnum.MOVIE.get_instance(app=app)
        results = app.api_fetcher.fetch_movies(title=title)
    elif selected_midia == 'series':
        MidiaInstance = MidiaEnum.SERIES.get_instance(app=app)
        results = app.api_fetcher.fetch_series(title=title)
    elif selected_midia == 'anime':
        raise NotImplementedError 
    else: 
        return None

    if not results:
        print("\n└─────────────> TMDB API search didn't find anything.")
        return None


    HEADERS = ["OPTIONS", "TITLE", "RELEASE DATE", "ID"]
    CONTENTS = categorize_contents(contents=results)

    option = interface.display_and_select(headers=HEADERS, contents=CONTENTS)
    if option == -1: # Exception from 'read_str()', return None
        return None
    

    # 'results' = ['Content Id', 'Title', 'Release Date', 'TMDB Id']
    info: List[str] = results[int(option) - 1]
    title: str = str(results[int(option) - 1][1])
    id: int = int(results[int(option) - 1][3])

    MidiaInstance.title = title

    files = DirectoryHandler.get_directory_files(app.directory_handler.selected_path)
    if type(MidiaInstance) == Movie:
        MidiaInstance.rename(files=files, info=info)


    elif type(MidiaInstance) == Series:

        seasons = app.api_fetcher.fetch_series_seasons(title=title, id=id)

        interface.display_msg_box(msg=f"{title.title()} SEASONS")
        HEADERS = ["OPTIONS", "SEASON NUMBER", "SEASON NAME", "EPISODE COUNT"]
        CONTENTS = categorize_contents(contents=seasons)

        option = interface.display_and_select(headers=HEADERS, contents=CONTENTS)
        if option == -1: # Exception from 'read_str()', return None
            return None

        # 'seasons' = ['Interface ID', 'Season Number', 'Season Name', 'Episode Count', 'TMDB Season Id']
        season_number = str(seasons[int(option) - 1][1])

        episodes = app.api_fetcher.fetch_series_episodes(series_id=id, season_number=season_number)

        MidiaInstance.rename(files=files, info=episodes)

    elif type(MidiaInstance) == Anime:
        raise NotImplementedError

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
        