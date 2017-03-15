import requests
import os
from dotenv import dot_env


class BookClient:
    def __init__(self, goodreads_key):
        self.endpoint = "https://www.goodreads.com/"
        self.api_key = goodreads_key





    def find_by_author(self, author):

        params = {
            "key": self.api_key
            "q": author,
        }

        return requests.get(self.endpoint, params=params)


    def find_by_genre(self, genre):

        params = {
            "key": self.api_key
            "q": genre,
        }

        return requests.get(self.endpoint, params=params)


    