from collections import defaultdict
from datetime import datetime
from typing import List, Optional
import requests
import json
import os
import sys
from pathlib import Path

def categorize_contents(
        *,
        contents: List[str], 
        identifiers: Optional[List[str]] = None

    ) -> List[List[str]]:
    # If 'identifiers' isn't provided.
    if not identifiers:

        identifiers = []
        for n in range(1, len(contents) + 1):
            # Assign default 'identifiers' based on the indices of 'contents', starting from 1
            identifiers.append(str(n))
        

    # Initialize an empty list to store the categorized contents.
    categorized_contents: List = []
    for i, content in enumerate(contents): 

        # Append a list containing the identifier and the content.
        categorized_contents.append([identifiers[i], str(content)])
    return categorized_contents 



class APIFetcher():

    __TOTAL_PAGES: int = 0

    def __init__(self, app) -> None:
        from Main import Main

        self.app: Main = app

        self.API_KEY = api_key
        self.USE_REAL_NAME = True
        self.MAX_SEARCH = 100


        self.__update()


    def __update(self) -> None:
        





    def fetch_movies(self, title: str):
        url = f'https://api.themoviedb.org/3/search/movie'
        page = 1
        total_pages = 1

        def get_params(page: int = 1) -> dict:
            params = {
                'api_key': self.API_KEY,
                'query': title,
                'include_adult': True,
                'page': page
                }
            
            return params

        def fetch(params, title: str):
            print("fetchin with params", params)
            response = requests.get(url, params=params)

            if response.status_code != 200:
                print(f"\nERROR - - -> RESPONSE STATUS CODE = {response.status_code}.")
                return -1
            
            data = response.json()
            if data['total_results'] == 0:
                print(f"\nERROR - - -> QUERY DIDN'T FIND ANYTHING WITH THE NAME {title}.")
                return -1
        
            infos: list[str, str, int, datetime] = []
            for results in data['results']:
                infos = [results['title'], results['original_title'], results['id'], results['release_date']]
                yield infos, data['total_pages']


        movies = []
        while page <= total_pages:
            params = get_params(page=page)
            page += 1

            for movie, total_pages in fetch(params=params, title=title):
                movies.append(movie)
                if len(movies) >= self.MAX_SEARCH:
                    return movies

                total_pages = total_pages











a = APIFetcher(api_key="251b2b4d1efc4b1061e752667bcf3cbf")

movies = a.fetch_movies(title="a")

b = categorize_contents(contents=movies)

for i, con in enumerate(b):
    print(i, con)

print(len(movies))