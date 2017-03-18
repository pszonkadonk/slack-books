import requests
from xml.etree import ElementTree
import os


class BookClient:
    def __init__(self, goodreads_key):
        self.endpoint = "https://www.goodreads.com/"
        self.api_key = goodreads_key


    def find_by_author(self, author):

        url = self.endpoint+'/search/index.xml?'

        params = {
            "key": self.api_key,
            "q": author
        }

        results = requests.get(url, params=params)
        root = ElementTree.fromstring(results.content)

        book_list = self.get_array_of_works(root)

        return book_list



    def find_by_genre(self, genre):

        params = {
            "key": self.api_key,
            "q": genre
        }

        return requests.get(self.endpoint, params=params)


    def get_array_of_works(self, xmlResult):
        work_list = []
        for work in xmlResult.iter('work'):
            work_dict = {}
            work_dict['review_count'] = work[3].text
            work_dict['publication_year'] = work[4].text
            work_dict['average_rating'] = work[7].text

            best_book = work[8]
            work_dict['book_id'] = best_book[0].text
            work_dict['book_title'] = best_book[1].text
            
            author = best_book[2]

            work_dict['author_id'] = author[0].text
            work_dict['author_name'] = author[1].text

            work_list.append(work_dict)
        
        return work_list
    
    def get_book_info_by_id(self, book_id):
        url = self.endpoint+'/book/show/'+str(book_id)+'.xml?'

        params = {
            "key": self.api_key
        }
        results = requests.get(url, params=params)
        root = ElementTree.fromstring(results.content)
        book_description = root[1][16].text


        return book_description