import requests
from xml.etree import ElementTree
import os
from bs4 import BeautifulSoup
import re

class BookClient:
    def __init__(self, goodreads_key):
        self.endpoint = "https://www.goodreads.com/"
        self.api_key = goodreads_key


    def find_by_author(self, author):
        """
        Make call to Goodreads to search for books
        by a particular author.  Parses the XML
        response and returns list of books
        """

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
        """
        Make call to Goodreads to search for books
        by a particular author.  Goodreads has no api call
        to search by genre, thus BeautifulSoup is used to 
        scrape book id's and then calls get_work to call Goodreads
        API to search by book and parse XML.  Limits to 15 books to 
        save time and resources
        """

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

    def find_most_popular(self):
        """
        Make call to Goodreads to search for books
        popular in the year 2017.  Goodreads has no api call
        to search by popular books, thus BeautifulSoup is used to 
        scrape book id's and then calls get_work to call Goodreads
        API to search by book and parse XML.  Limits to 15 books to 
        save time and resources
        """
        book_list_ids = []
        book_list =[]
        r = requests.get(self.endpoint+"book/popular_by_date/2017")
        soup = BeautifulSoup(r.content, 'html.parser')

        for book in soup.find_all('div', class_='u-anchorTarget'):
            book_id = book.get('id')
            book_list_ids.append(book_id)

        book_list_ids = book_list_ids[0:15]   # limit selection to 15 book


        for id in book_list_ids:
            book_xml = self.get_book_by_id(id)
            self.get_work(book_xml)
            book_list.append(self.get_work(book_xml))
            

        return book_list

    def find_similar_author(self, author):
        """
        Returns an list of authors that are similar to the author
        that the user provided 
        """
        author = author.replace("."," ")
        similar_author_list = []
        author_id = self.find_author_id(author)
        url = self.endpoint + "author/similar/" + author_id + "." + author
        results = requests.get(url)
        soup = BeautifulSoup(results.content, 'html.parser')

        for authors in soup.find_all('div', class_='readable'):
            author_name = authors.find('a', 'bookTitle').contents[0]
            similar_author_list.append(author_name)
        
        similar_author_list = similar_author_list[1:]  #remove original author

        return similar_author_list



    def find_author_id(self, author):
        """
        Makes call to Goodreads api to search
        an author by name and return the author id
        """
        params = {
            "key": self.api_key
        }

        url = self.endpoint + "api/author_url/" + author
        results = requests.get(url, params=params)
        print(results.url)
        root = ElementTree.fromstring(results.content)
        author_id  = root[1].attrib['id']

        return author_id

    def find_similar_books(self, book):
        """
        Returns an list of books that are similar to the book
        that the user provided 
        """
        book = re.sub(r'[^\w\s]', ' ', book)
        book = book.split(' ')
        book = re.sub(r'--','-','-'.join(book))

        similar_book_list = []
        book_id = self.find_book_id(book)
        url = self.endpoint + "book/similar/" + book_id + "-"+ book
        results = requests.get(url)

        soup = BeautifulSoup(results.content, "html.parser")

        for book in soup.find_all('a', class_='bookTitle'):
            book_title = book.find('span').text
            similar_book_list.append(book_title)


        return similar_book_list




    def find_book_id(self, book):
        """
        Returns an list of books that are similar to the book
        that the user provided 
        """
        params = {
            "key": self.api_key,
            "q": book
        }

        url = self.endpoint + "search/index.xml"
        results = requests.get(url, params=params)

        root = ElementTree.fromstring(results.content)
        work = root[1][6]
        book_id = work[0][0].text

        return book_id


    
    def get_work(self, bookXmlResult):
        """
        Parse XML response for a book and return the 
        title, id, review_count, publication_year, author_id
        author_name, and average_rating.  Returns dictionary
        for individual book
        """
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
        """
        Called after author search API call is made.
        Parses XML response and returns each book (work)
        from an author
        """
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
        """
        Makes call to Goodreads API to search
        for a particular book by its id.  Returns
        XML response 
        """        
        book_dict = {}
        url = self.endpoint+'/book/show/'+str(book_id)+'.xml?'
        params = {
            "key": self.api_key
        }

        results = requests.get(url, params=params)
        root = ElementTree.fromstring(results.content)

        return root


    
    def get_book_info_by_id(self, book_id):

        """
        Makes call to Goodreads API to search
        for a particular book by its id.  Returns
        only the description for a book 
        """   
        url = self.endpoint+'/book/show/'+str(book_id)+'.xml?'

        params = {
            "key": self.api_key
        }
        results = requests.get(url, params=params)
        root = ElementTree.fromstring(results.content)
        book_description = root[1][16].text


        return book_description