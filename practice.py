import requests
from xml.etree import ElementTree
from book import BookClient

my_client = BookClient('GUlqkpreN4ptYlQfhKt6A')

# foo = my_client.find_by_author('John Steinbeck')
# context = {}
# context['books'] = foo

# for i, book in enumerate(context['books']):
#     print(str(i+1) + ". " + book['book_title'])



my_client.get_book_info_by_id('4406')




# api_key = 'GUlqkpreN4ptYlQfhKt6A'

# endpoint = 'http://goodreads.com/search/index.xml'
# params = {
#     "key": api_key,
#     "q": "Ender's Game",
# }



# r = requests.get(endpoint, params = params)
# root = ElementTree.fromstring(r.content)

# work_list = []
# for work in root.iter('work'):
#     work_dict = {}
#     work_dict['book_id'] = work[0].text
#     work_dict['review_count'] = work[3].text
#     work_dict['publication_year'] = work[4].text
#     work_dict['average_rating'] = work[7].text

#     best_book = work[8]
#     work_dict['book_title'] = best_book[1].text
    
#     author = best_book[2]

#     work_dict['author_id'] = author[0].text
#     work_dict['author_name'] = author[1].text

#     work_list.append(work_dict)

# print(work_list)