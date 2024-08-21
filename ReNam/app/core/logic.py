import os
from pathlib import Path
import re
import copy
from app.classes.handlers.interface_handler import InterfaceHandler
from app.classes.handlers.directory_handler import DirectoryHandler
from typing import List, Optional, Tuple, Union
from app.core.exceptions import APIFetcherException
from app.classes.handlers.midia_handler import Anime, MidiasEnum, Movie, Series
from app.assets.utils.inputs import read_str
from app.assets.utils.generics import categorize_contents
from main import Main


def find_paths(app: Main) -> Union[List[Path], None]:

    value = read_str(msg="\nInsert full path or directory name: ")
    if value == -1: # Exception from 'read_str()'
        return None
    
    try:
        path: Path = Path(value).resolve()
    except Exception as exc:
        print(f"\n└─────────────> Couldn't get a Path object out of ['{value}']\n")
        return None
    
    print(f"\n└─────────────> Please wait while ['{path}'] is being searched...\n")
    search = app.directory_handler.search_drives(path=path)
    if search is None:
        print(f"\n└─────────────> The directory path ['{path}'] wasn't found.\n")
        return None
    
    return search
    

def select_path(app: Main, paths: Optional[List[Path]] = None) -> Union[Path, None]:

    if paths is None:
        paths = find_paths(app=app)

    if len(paths) == 0 or paths is None:
        return None

    # If 'paths' contains a single path
    if len(paths) == 1:               
        return paths[0]

    paths_as_str: List[str] = []
    for i in range(len(paths)):
        paths_as_str.append(str(paths[i]))

    headers = ["OPTIONS", "PATHS"]
    contents = categorize_contents(contents=paths_as_str)

    option = app.interface_handler.display_and_select(headers=headers, contents=contents)
    if option == -1: # Exception from 'display_and_select()'
        return None

    return paths[int(option) - 1]
    

def select_midia(app: Main) -> Union[str, None]:

    midias = MidiasEnum.list_all()
    headers = ["OPTIONS", "MIDIA TYPE"]
    contents = categorize_contents(contents=midias)

    option = app.interface_handler.display_and_select(headers=headers, contents=contents)
    if option == -1: # Exception from 'display_and_select()'
        return None
    
    return midias[int(option) - 1].lower()


def rename(app: Main) -> None:

    midia = select_midia(app=app)
    if not midia:
        return None
    
    midia_title = read_str(msg=f"\n└─────────────> Insert a {midia} title: ")
    if midia_title == -1: # Exception from 'read_str()'
        return None
    

    if midia ==  "movie":
        movies_results = app.api_fetcher.fetch_movies(title=midia_title)
        if not movies_results:
            print("\n└─────────────> 'APIFetcher' search didn't find anything.")
            return None
        
        headers = ["OPTIONS", "TITLE", "RELEASE DATE", "ID"]
        contents = categorize_contents(movies_results)

        option = app.interface_handler.display_and_select(headers=headers, contents=contents)
        if option == -1: # Exception from 'display_and_select()'
            return None

        # NOTE: movie_info = ['Title', 'Release Date', 'TMDB ID']
        movie_info = movies_results[int(option) - 1] 

        rename_movie(app=app, result=movie_info)


    elif midia == "anime":
        midia_instance = MidiasEnum.ANIME.get_instance(app=app)
        #     # TODO: Implement Animes rename logic
        #     # NOTE: Anime logic is more complex


    elif midia == "series":
        series_results = app.api_fetcher.fetch_series(title=midia_title)
        if not series_results:
            print("\n└─────────────> 'APIFetcher' search didn't find anything.")
            return None

        headers = ["OPTIONS", "TITLE", "RELEASE DATE", "ID"]
        contents = categorize_contents(series_results)

        
        option = app.interface_handler.display_and_select(headers=headers, contents=contents)
        if option == -1: # Exception from 'display_and_select()'
            return None
        
        # NOTE: series_info = ['Title', 'Release Date', 'TMDB ID']
        series_info = series_results[int(option) - 1]
        series_title = series_info[0]
        series_id = series_info[2]
        

        # TV Shows may or may not have episode groups
        episode_groups_results = app.api_fetcher.fetch_series_episode_groups(series_id=series_id, title=series_title)
        if not episode_groups_results:
            option = 'DEFAULT GROUP'
        else:
            headers = ["OPTIONS", "NAME"]
            contents = categorize_contents(["DEFAULT GROUP", "EPISODE GROUPS"])

            app.interface_handler.display_msg_box(msg=f"{series_title.title()} POSSIBLE OPTIONS")
            option = app.interface_handler.display_and_select(headers=headers, contents=contents, index=1)
            if option == -1: # Exception from 'display_and_select()'
                return None
            

        if option == "DEFAULT GROUP":
            
            # NOTE: seasons = [['Season number', 'Season name', 'Episode count'], ... ]
            seasons = app.api_fetcher.fetch_series_seasons(title=series_title, id=series_id)

            headers = ["OPTIONS", "SEASON NUMBER", "SEASON NAME", "EPISODE COUNT"]
            contents = categorize_contents(seasons)

            app.interface_handler.display_msg_box(msg=f"{series_title.title()} SEASONS")
            option = app.interface_handler.display_and_select(headers=headers, contents=contents)
            if option == -1: # Exception from 'display_and_select()'
                return None

            season_number = str(seasons[int(option) - 1][0])
            season_episodes = app.api_fetcher.fetch_series_episodes(series_id=series_id, season_number=season_number)
            
        elif option == "EPISODE GROUPS":

            headers = ["OPTIONS", "TITLE", "EPISODE COUNT", "ID"]
            contents = categorize_contents(episode_groups_results)

            option = app.interface_handler.display_and_select(headers=headers, contents=contents)
            if option == -1: # Exception from 'display_and_select()'
                return None

            # NOTE: group_info = ['Title', 'Episode count', 'TMDB ID']
            group_info = episode_groups_results[int(option) - 1]
            group_id = group_info[2]

            # NOTE: group_info = [['name', 'episode_count', episodes['name', 'ep_number', 'season_number']], ... ]     
            group_info = app.api_fetcher.fetch_series_group(group_id=group_id, title=series_title)

            headers = ["OPTIONS", "TITLE", "EPISODE COUNT"]
            contents = categorize_contents(contents=[[info[0], info[1]] for info in group_info])

            app.interface_handler.display_msg_box(msg=f"{series_title.title()} GROUPS")
            option = app.interface_handler.display_and_select(headers=headers, contents=contents)
            if option == -1: # Exception from 'display_and_select()'
                return None
            
            # NOTE: maybe?
            season_info = group_info[int(option) - 1]
            season_number = season_info[2][0][2]
            season_episodes = season_info[2]

        rename_series(app=app, title=series_title, season=season_number, episodes_info=season_episodes)


def rename_movie(app: Main, result: List) -> None:
    interface: InterfaceHandler = app.interface_handler
    movie = MidiasEnum.MOVIE.get_instance(app=app)

    files = DirectoryHandler.get_directory_files(app.directory_handler.selected_path)
    files = DirectoryHandler.filter_files(files=files, formats=movie.files_extensions)

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
    files = DirectoryHandler.filter_files(files=files, formats=series.files_extensions)
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
    if total_results != len(episodes): # ordered_files
        print(f"\n'extract_eps_order' failed when extracting episodes order from API")
        return None
    
    series.episodes = ordered_episodes
    # if len(series.episodes) != len(ordered_files):
    #     # TODO: maybe rename???
    #     print(f"not enough correspondencies to rename")
    #     return None
   
    old_paths: List[Path] = []
    new_paths: List[Path] = []
    for key, values in ordered_files.items():
        name = series.episodes.get(key, None)[0]
        if name is None:
            print("Missing episode name")

        name = series.title + " " + name
        name = re.sub(r'[<>:"/\\|?*]', '', name)


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
    raise NotImplementedError()
    