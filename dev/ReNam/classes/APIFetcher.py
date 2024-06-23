from typing import Any, Dict, Generator, List, Tuple, Union
import requests
from requests import Response
from classes.Exceptions import APIFetcherException



class APIFetcher():

    __BASE_URL: str = "https://api.themoviedb.org/3/search"

    __current_page: int = 1
    __total_pages: int = 1
   
    def __init__(self, app) -> None:
        from Main import Main

        self.app: Main = app

        self.API_KEY: str = ""
        self.MAX_SEARCH: int = 0


        self.update()

    
    def update(self) -> None:
        configs = self.app.configs

        self.API_KEY = configs.api_key
        self.MAX_SEARCH = configs.max_search

    
    def __reset(self) -> None:
        self.current_page = 1
        self.total_pages = 1


    def __make_request(self, *, endpoint: str, params: dict) -> Tuple[int, Dict]:
        url: str = f"{self.BASE_URL}/{endpoint}"
        
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
    

    def fetch_movies(self, title: str) -> Any:
        endpoint: str = "movies"


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

            finally:
                self.__reset()


        return movies
                
                


            
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



