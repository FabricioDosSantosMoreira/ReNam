from typing import Any, Dict, Generator, List, Tuple, Union
import requests
from requests import Response
from app.core.exceptions import APIFetcherException



class APIFetcher():

    __BASE_URL: str = "https://api.themoviedb.org/3/"

    __current_page: int = 1
    __total_pages: int = 1
   
    def __init__(self, app) -> None:
        from main import Main

        self.app: Main = app

        self.API_KEY: str = ""
        self.MAX_SEARCH: int = 0


        self.update()

    
    def update(self) -> None:
        configs = self.app.config_handler

        self.API_KEY = configs.api_key
        self.MAX_SEARCH = configs.max_search

    
    def __reset(self) -> None:
        self.current_page = 1
        self.total_pages = 1


    def __make_request(self, *, endpoint: str, params: dict) -> Tuple[int, Dict]:
        url: str = f"{self.BASE_URL}{endpoint}"

        response: Response = requests.get(url=url, params=params)

        return response.status_code, response.json()


    def __make_params(self, query: str, page: int) -> Dict:
        params = {
            'query': query,
            'page': page,
            'api_key': self.API_KEY,
            'include_adult': True
        }

        return params
    

    def fetch_movies(self, title: str) -> List[Union[List[str], None]]:
        endpoint: str = "search/movie"


        def fetch() -> Generator[List[str], None, None]:
            params = self.__make_params(query=title, page=self.current_page)

            status_code, data = self.__make_request(endpoint=endpoint, params=params)
            if status_code != 200:
                raise APIFetcherException(
                    message=f"RESPONSE STATUS CODE = {status_code}."
                )
            
            elif data['total_results'] == 0:
                raise APIFetcherException(
                    message=f"QUERY DIDN'T FIND ANYTHING WITH THE NAME {title}."
                )
            

            self.total_pages = data['total_pages']
            
            for result in data['results']:
                info = [str(result['title']), str(result['release_date']), str(result['id'])]
                yield info


        movies: List[List[str]] = []
        while self.current_page <= self.total_pages:
            try:
                for movie in fetch():
                    movies.append(movie)
                    if len(movies) >= self.MAX_SEARCH:
                        break  
                else:
                    self.current_page += 1
                    continue  
                break 
        
            except APIFetcherException as exc:
                break


        self.__reset()
        return movies
    

    def fetch_series(self, title: str) -> List[Union[List[str], None]]:
        endpoint: str = "search/tv"


        def fetch() -> Generator[List[str], None, None]:
            params = self.__make_params(query=title, page=self.current_page)

            status_code, data = self.__make_request(endpoint=endpoint, params=params)
            if status_code != 200:
                raise APIFetcherException(
                    message=f"RESPONSE STATUS CODE = {status_code}."
                )
            
            elif data['total_results'] == 0:
                raise APIFetcherException(
                    message=f"QUERY DIDN'T FIND ANYTHING WITH THE NAME {title}."
                )
            

            self.total_pages = data['total_pages']
            
            for result in data['results']:
                info = [str(result['name']), str(result['first_air_date']), str(result['id'])]
                yield info


        series: List[List[str]] = []
        while self.current_page <= self.total_pages:
            try:
                for s in fetch():
                    series.append(s)
                    if len(series) >= self.MAX_SEARCH:
                        break  
                else:
                    self.current_page += 1
                    continue  
                break 
        
            except APIFetcherException as exc:
                break


        self.__reset()
        return series


    def fetch_series_seasons(self, title: str, id: str):
        endpoint: str = f"tv/{id}"

        def fetch() -> Generator[List[str], None, None]:
            params = {'api_key': self.API_KEY}

            status_code, data = self.__make_request(endpoint=endpoint, params=params)
            if status_code != 200:
                raise APIFetcherException(
                    message=f"RESPONSE STATUS CODE = {status_code}."
                )
            
            elif not data:
                raise APIFetcherException(
                    message=f"QUERY DIDN'T FIND ANYTHING WITH THE NAME {title}."
                )
   
            for season in data['seasons']:
                info = [str(season['season_number']), str(season['name']), str(season['episode_count'])]
                yield info


        seasons: List[str] = []
        for season in fetch():
            seasons.append(season)


        self.__reset()
        return seasons
  

    def fetch_series_episodes(self, series_id: str, season_number: str):
        endpoint: str = f"tv/{series_id}/season/{season_number}"


        def fetch() -> Generator[List[str], None, None]:
            params = {'api_key': self.API_KEY}

            status_code, data = self.__make_request(endpoint=endpoint, params=params)
            if status_code != 200:
                raise APIFetcherException(
                    message=f"RESPONSE STATUS CODE = {status_code}."
                )
            
            elif not data:
                raise APIFetcherException(
                    message=f"QUERY DIDN'T FIND ANYTHING WITH THE ID {series_id}."
                )
   
            for episode in data['episodes']:
                info = [str(episode['name']), str(episode['episode_number']), str(episode['season_number'])]
                yield info


        episodes: List[str] = []
        for episode in fetch():
            episodes.append(episode)


        self.__reset()
        return episodes


    def fetch_series_episode_groups(self, series_id: int, title: str) -> List[List[str]]:
        endpoint=f"tv/{series_id}/episode_groups"


        def fetch() -> Generator[List[str], None, None]:
            params={'api_key': self.API_KEY}

            status_code, data = self.__make_request(endpoint=endpoint, params=params)
            if status_code != 200:
                raise APIFetcherException(
                    message=f"RESPONSE STATUS CODE = {status_code}."
                )
            
            elif len(data['results']) == 0:
                raise APIFetcherException(
                    message=f"QUERY DIDN'T FIND A EPISODE GROUP FOR {title}."
                )
            
            for info in data['results']:
                yield [str(info['name']), str(info['episode_count']), str(info['id'])]

        
        groups_info = []
        try:
            for group_info in fetch():
                groups_info.append(group_info)

        except APIFetcherException as exc:
            pass 

        return groups_info


    def fetch_series_group(self, group_id: str, title: str):
        endpoint: str = f"tv/episode_group/{group_id}"

        def fetch():
            params = {'api_key': self.API_KEY}
            status_code, data = self.__make_request(endpoint=endpoint, params=params)

            if status_code != 200:
                raise APIFetcherException(
                    message=f"RESPONSE STATUS CODE = {status_code}."
                )

            elif not data:
                raise APIFetcherException(
                    message=f"QUERY DIDN'T FIND ANYTHING WITH THE NAME {title}."
                )

            groups_count = data['group_count']
            # group_episodes_count = data['episode_count']
            
            for group in range(groups_count):
                group_data =  data['groups'][group]

                season_name = group_data['name']
                episode_count = len(group_data['episodes'])
                episodes: List = []

                for ep in range(episode_count): 
                    ep_name = str(group_data['episodes'][ep]['name'])
                    ep_number = str(group_data['episodes'][ep]['episode_number'])
                    season_number = str(group_data['episodes'][ep]['season_number'])

                    episodes.append([ep_name, ep_number, season_number])

                group_info = [str(season_name), str(episode_count), episodes]
                yield group_info

        # [['name', 'episode_count', 'episodes['name', 'ep_number', 'season_number']'], ... ]        
        group_info: List = []
        try:
            for info in fetch():
                group_info.append(info)

        except APIFetcherException as exc:
            pass 
        
        return group_info

            
    @property
    def BASE_URL(self) -> str:
        return self.__BASE_URL
    
    @property
    def total_pages(self) -> int:
        return self.__total_pages
    @total_pages.setter
    def total_pages(self, value: int) -> None:
        self.__total_pages = value

    @property
    def current_page(self) -> int:
        return self.__current_page
    @current_page.setter
    def current_page(self, value: int) -> None:
        self.__current_page = value



