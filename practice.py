import requests
from xml.etree import ElementTree


api_key = 'GUlqkpreN4ptYlQfhKt6A'

endpoint = 'http://goodreads.com/search/index.xml'
params = {
    "key": api_key,
    "q": "Ender's Game",
}



r = requests.get(endpoint, params = params)
root = ElementTree.fromstring(r.content)

results = root[1][6]

arr = []
for title in root.iter('title'):
    arr.append(title.text)


print(arr)

# for work in results.findall('work'):
#     book = work.find('best_book')
#     title = book.find('title').text
#     print(title)
