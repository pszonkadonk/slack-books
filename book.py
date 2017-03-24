import requests
from xml.etree import ElementTree
import os
from bs4 import BeautifulSoup


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

        book_list_ids = []
        book_list =[]
        r = requests.get(self.endpoint+"genres/"+genre)
        soup = BeautifulSoup(r.content, 'html.parser')

        for book in soup.find_all('div', class_='coverWrapper'):
            book_id = book.get('id').split('_')[1]
            book_list_ids.append(book_id)

        book_list_ids = book_list_ids[0:15]   # limit selection to 15 book

        for id in book_list_ids:
            book_xml = self.get_book_by_id(id)
            self.get_work(book_xml)
            book_list.append(self.get_work(book_xml))
            

        return book_list
        

    def get_work(self, bookXmlResult):
        book_dict = {}
        book_work = bookXmlResult[1][17]
        book_author = bookXmlResult[1][26]
        
        book_dict['book_title'] = bookXmlResult[1][1].text
        book_dict['book_id'] = book_work[2].text
        book_dict['review_count'] = book_work[3].text
        book_dict['publication_year'] = book_work[7].text


        book_dict['author_id'] = book_author[0][0].text
        book_dict['author_name'] = book_author[0][1].text


        book_dict['average_rating'] = bookXmlResult[1][18].text

        return book_dict

    



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

    def get_book_by_id(self, book_id):

        book_dict = {}
        url = self.endpoint+'/book/show/'+str(book_id)+'.xml?'
        params = {
            "key": self.api_key
        }

        results = requests.get(url, params=params)
        root = ElementTree.fromstring(results.content)

        # book_dict['book_title'] = root[1][1].text
        # book_dict['description'] = root[1][16].text

        return root


    
    def get_book_info_by_id(self, book_id):

        url = self.endpoint+'/book/show/'+str(book_id)+'.xml?'

        params = {
            "key": self.api_key
        }
        results = requests.get(url, params=params)
        root = ElementTree.fromstring(results.content)
        book_description = root[1][16].text


        return book_description