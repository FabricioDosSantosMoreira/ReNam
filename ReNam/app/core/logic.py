import os
from pathlib import Path
import re
from app.classes.handlers.interface_handler import InterfaceHandler
from app.classes.handlers.directory_handler import DirectoryHandler
from typing import List, Optional, Union
from app.core.exceptions import APIFetcherException
from app.classes.handlers.midia_handler import Anime, MidiasEnum, Movie, Series
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
    

def select_path(app: Main, paths: Optional[List[Path]] = None) -> Union[Path, None]:
    interface: InterfaceHandler = app.interface_handler

    if not paths:
        paths = read_path(app=app)


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
    

def select_midia(app: Main) -> Union[str, None]:
    interface: InterfaceHandler = app.interface_handler

    MIDIAS = MidiasEnum.list_all()
    HEADERS = ["OPTIONS", "MIDIA TYPE"]
    CONTENTS = categorize_contents(contents=MIDIAS)

    option = interface.display_and_select(headers=HEADERS, contents=CONTENTS)
    if option == -1: # Exception from 'read_str()', return None
        return None
    
    midia = str(MIDIAS[int(option) - 1]).lower()

    return midia


def select_single_result(app: Main, results: List) -> List:
    interface: InterfaceHandler = app.interface_handler

    HEADERS = ["OPTIONS", "TITLE", "RELEASE DATE", "ID"]
    CONTENTS = categorize_contents(contents=results)

    option = interface.display_and_select(headers=HEADERS, contents=CONTENTS)
    if option == -1: # Exception from 'read_str()', return None
        return None
    
    # NOTE: 'results' = [['Content Id', 'Title', 'Release Date', 'TMDB Id'], ...]
    result = results[int(option) - 1]
    
    return result


def rename(app: Main) -> None:
    interface: InterfaceHandler = app.interface_handler

    midia = select_midia(app=app)
    if not midia:
        return None
    
    title = read_str(msg=f"\n└─────────────> Insert a {midia} title: ")
    if title == -1: # Exception from 'read_str()', return None
        return None
    
    if midia == "anime":
        midia_instance = MidiasEnum.ANIME.get_instance(app=app)
        # TODO: Implement Animes rename logic
        # NOTE: Anime logic is more complex

    elif midia == 'movie':
        results = app.api_fetcher.fetch_movies(title=title)
        if not results:
            print("\n└─────────────> 'APIFetcher' search didn't find anything.")
            return None

        result = select_single_result(app=app, results=results)
        rename_movie(app=app, result=result)

    elif midia == 'series':
        results = app.api_fetcher.fetch_series(title=title)
        if not results:
            print("\n└─────────────> 'APIFetcher' search didn't find anything.")
            return None

        result = select_single_result(app=app, results=results)

        id = result[3]
        title = result[1]
        seasons = app.api_fetcher.fetch_series_seasons(title=title, id=id)

        interface.display_msg_box(msg=f"{title.title()} SEASONS")
        HEADERS = ["OPTIONS", "SEASON NUMBER", "SEASON NAME", "EPISODE COUNT"]
        CONTENTS = categorize_contents(contents=seasons)

        option = interface.display_and_select(headers=HEADERS, contents=CONTENTS)
        if option == -1: # Exception from 'read_str()', return None
            return None

        # 'seasons' = ['Content ID', 'Season Number', 'Season Name', 'Episode Count', 'TMDB Season Id']
        season_number = str(seasons[int(option) - 1][1])

        episodes = app.api_fetcher.fetch_series_episodes(series_id=id, season_number=season_number)

        rename_series(app=app, title=title, season=season_number, episodes_info=episodes)


def rename_movie(app: Main, result: List) -> None:
    interface: InterfaceHandler = app.interface_handler
    movie = MidiasEnum.MOVIE.get_instance(app=app)

    files = DirectoryHandler.get_directory_files(app.directory_handler.selected_path)
    files = DirectoryHandler.filter_files(files=files, formats=movie.file_extensions)

    if files:
        # NOTE: 'result' = ['Content Id', 'Title', 'Release Date', 'TMDB Id']
        movie.title = result[1]
        movie.launch_date = result[2]
        
        name: str = f"{movie.title} - {movie.launch_date}"
        name = re.sub(r'[<>:"/\\|?*]', '', name)


        old_files: List[Path] = []
        new_files: List[Path] = []
        for i in range(len(files)):
            old_files.append(files[i])
            new_files.append(Path(files[i].parent / (name + files[i].suffix)))

        HEADERS = ["OLD NAMES", "NEW NAMES"]
        CONTENTS = []
        for i in range(len(files)):
            CONTENTS.append([old_files[i].name, new_files[i].name])
        interface.display_interface(headers=HEADERS, contents=CONTENTS)

        value = input("press y to rename, else cancel: ")
        if str(value).lower() == "y":
            for i, file in enumerate(files):
                src = file
                dst = Path(f"{file.parent}/{name}{file.suffix}")

                os.rename(src=src, dst=dst)

    else:
        print("ERROR. No files to rename")

        
def rename_series(app: Main, title: str, season: str, episodes_info: List) -> None:
    interface: InterfaceHandler = app.interface_handler

    root_path: Path = app.directory_handler.selected_path

    series = MidiasEnum.SERIES.get_instance(app=app)

    files = DirectoryHandler.get_directory_files(app.directory_handler.selected_path)
    files = DirectoryHandler.filter_files(files=files, formats=series.file_extensions)
    files_names = DirectoryHandler.get_path_name(paths=files)

    ordered_files, total_results = series.extract_eps_order(files=files_names)
    if total_results != len(files):
        print(f"\n'extract_eps_order' failed when extracting files order")
        return None

    series.title = title
    series.season = season

    episodes = []
    for i in range(len(episodes_info)):
        # episodes_info = ['ep_name', 'ep_num', 'ep_season']
        if len(episodes_info[i][1]) <= 1:
            ep_num = f"0{episodes_info[i][1]}"
        else: 
            ep_num = episodes_info[i][1]
            
        ep_name = re.sub(r'[<>:"/\\|?*]', '', episodes_info[i][0])

        episodes.append(f"S{series.season}E{ep_num} - {ep_name}")


    ordered_episodes, total_results = series.extract_eps_order(files=episodes)
    if total_results != len(ordered_files):
        print(f"\n'extract_eps_order' failed when extracting episodes order from API")
        return None
    
    series.episodes = ordered_episodes
    if len(series.episodes) != len(ordered_files):
        # TODO: maybe rename???
        print(f"not enough correspondencies to rename")
        return None
   
    old_paths: List[Path] = []
    new_paths: List[Path] = []
    for key, values in ordered_files.items():
        name = series.episodes.get(key, None)[0]
        if name is None:
            print("Missing episode name")

        name = series.title + " " + name

        for value in values:
            old_paths.append(Path(root_path / value))
            new_paths.append(Path(root_path / (name + DirectoryHandler.get_path_suffix(paths=[value])[0])))


    if len(old_paths) != len(new_paths):
        print("Couldn't rename. Missing paths correspondencies")

    HEADERS = ["OLD FILE NAMES", "NEW FILES NAMES"]
    CONTENTS = []
    for i in range(len(old_paths)):
        CONTENTS.append([old_paths[i].name, new_paths[i].name])

    interface.display_interface(headers=HEADERS, contents=CONTENTS)
    value = input("press y to rename, else cancel: ")

    if str(value).lower() == "y":
        for i in range(len(old_paths)):
            if old_paths[i].exists():
                os.rename(old_paths[i], new_paths[i])
            else:
                print(f"{old_paths[i]} does not exist")



















def rename_anime() -> None:
    raise NotImplementedError
    
#     # # Seleciona o episode-group
#     # groups = app.api_fetcher.fetch_series_episode_groups(series_id=id, title=title)

#     # HEADERS = ["OPTIONS", "NAME", "EPISODE COUNT", "GROUP ID"]
#     # CONTENTS = categorize_contents(contents=groups)

#     # app.interface_handler.display_msg_box(msg="EPISODE GROUPS")
#     # option = app.interface_handler.display_and_select(headers=HEADERS, contents=CONTENTS)
#     # if option == -1: # Exception from 'read_str()', return None
#     #     return None
    
#     # # 'groups' = ['Content Id', 'Name', 'Episode Count', 'TMDB Ep. Group Id']
#     # group_id = str(groups[int(option) - 1][3])

#     # seasons = app.api_fetcher.fetch_series_group(group_id=group_id, title=title)

#     # #app.api_fetcher.fetch_seasons(series_id=id, seasons=seasons)
#     pass