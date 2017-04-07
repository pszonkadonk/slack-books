from book import BookClient

my_client = BookClient('GUlqkpreN4ptYlQfhKt6A')

print(my_client.find_most_popular())


# books = my_client.find_by_author('John Steinbeck')

# books = my_client.find_by_genre('History')


# for book in books:
#     print(book['book_title'])
#     print(book['book_id'])
#     print(book['review_count'])
#     print(book['publication_year'])


#     print(book['author_id'])
#     print(book['author_name'])


#     print(book['average_rating'])


