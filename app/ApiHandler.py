import requests
import json

API_KEY = 'YOUR_API_KEY_HERE'
USE_REAL_NAME = True

def get_midia_name(ordered_dict_files: dict[int, str], midia_type: str, midia_name: str, season: int, start_from: int=0):
    # ordered_dict_files{ep_number, "file name"}

    if not midia_type:
        print("\nERROR - - -> NO MIDIA TYPE FOUND.")
    
    else:
        if midia_type == 'tv':
            names = get_tv_names(ordered_dict_files, start_from, midia_name, season)
            return names
            
        elif midia_type == "movie":
            name = get_movie_name(midia_name)
            return name
        

def get_movie_name(name):

    movie_name = []

    url = f'https://api.themoviedb.org/3/search/movie'

    params = {
            'api_key': API_KEY,
            'query': name
            }

    response = requests.get(url, params=params)

    if not response.status_code == 200:
        print(f"\nERROR - - -> RESPONSE STATUS CODE = {response.status_code}.")

    else:
        data = response.json()

        if data['total_results'] == 0:
            print(f"\nERROR - - -> QUERY DIDN'T FIND ANYTHING WITH THE NAME {name}.")

        else:
            from Interface import Interface
            interface = Interface()

            names = [results['title'] for results in data['results']]
            selected_result = interface.select_from_list(names, "MOVIE RESULTS")

            for results in data['results']:
                if results['title'] == selected_result:
                    id = results['id']
                    break

            if id:
                try:
                    detail_url = f"https://api.themoviedb.org/3/movie/{id}"
                    detail_params = {
                        'api_key': API_KEY,
                    }
                    detail_response = requests.get(detail_url, params=detail_params)

                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()

                        print(detail_data)
                        print(detail_data['release_date'][:4])
                        print(detail_data['title'])

                        movie_name.append(detail_data['title'] + " " + str(detail_data['release_date'][:4]))

                except KeyError:
                    print("\nERROR - - -> KeyError.")

    print("nome do filme", movie_name)
    return movie_name


def get_tv_names(ordered_dict_files: dict[str, int], start_from, name, season):

    url = f'https://api.themoviedb.org/3/search/tv'
    params = {
            'api_key': API_KEY,
            'query': name
            }

    episodes_names = []

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data['total_results'] == 0:
            print(f"\nERROR - - -> QUERY DIDN'T FIND ANYTHING WITH THE NAME {name}.")

        else: 
            # IF THERE ARE MULTIPLE RESULTS FOR A NAME, THE USER HAVE TO SELECT 
            from Interface import Interface
            interface = Interface()
                      
            names = [result['name'] for result in data['results']]
            selected_result = interface.select_from_list(names, "TV RESULTS")

            real_name = name

            for results in data['results']:
                if results['name'] == selected_result:
                    if USE_REAL_NAME:
                        real_name = results['name']
                    id = results['id']
                    break



            if start_from == 0:
                start_from = 1

            # + start from = len(kys) - start
            for ep in range(start_from, len(ordered_dict_files.keys()) + start_from):
                try:
                    detail_url = f"https://api.themoviedb.org/3/tv/{id}/season/{season}/episode/{ep}"
                    detail_params = {
                        'api_key': API_KEY,
                    }
                    detail_response = requests.get(detail_url, params=detail_params)

                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()

                        if season <= 9:
                            season_str = "0" + str(season)
                        else:
                            season_str = season

                        if ep <= 9:
                            ep= "0" + str(ep)

                        episodes_names.append(f"{real_name} S{season_str}E{ep} {detail_data['name']}")
                        print(f"\nEPISODE [{ep}] NAME = [{detail_data['name']}]")
                
                    else:
                        print(f"\nERROR - - -> RESPONSE STATUS CODE = {detail_response.status_code}.")
                        break

                except KeyError:
                    print("\nERROR - - -> KeyError.")
                    break
    else:
        print(f"\nERROR - - -> RESPONSE STATUS CODE = {response.status_code}.")

    
    print(episodes_names)
    return episodes_names

   