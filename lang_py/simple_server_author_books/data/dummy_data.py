from functools import reduce

"""
Learning from Node.js tutorial:
https://github.com/WebDevSimplified/Learn-GraphQL/blob/master/server.js
"""

#
# Dummy data
#

authors = [{"id": 1, "name": 'J. K. Rowling'},
           {"id": 2, "name": 'J. R. R. Tolkien'},
           {"id": 3, "name": 'Brent Weeks'}]

books = [{"id": 1, "name": 'Harry Potter and the Chamber of Secrets', "authorId": 1},
         {"id": 2, "name": 'Harry Potter and the Prisoner of Azkaban', "authorId": 1},
         {"id": 3, "name": 'Harry Potter and the Goblet of Fire', "authorId": 1},
         {"id": 4, "name": 'The Fellowship of the Ring', "authorId": 2},
         {"id": 5, "name": 'The Two Towers', "authorId": 2},
         {"id": 6, "name": 'The Return of the King', "authorId": 2},
         {"id": 7, "name": 'The Way of Shadows', "authorId": 3},
         {"id": 8, "name": 'Beyond the Shadows', "authorId": 3}]


#
# Accessors for dummy data
#

def get_author_from_id(a_id):
    return next(filter(lambda author: author['id'] == a_id, authors))


def get_book_from_id(b_id):
    return next(filter(lambda book: book['id'] == b_id, books))


def get_books_from_author_id(a_id):
    return list(filter(lambda book: book['authorId'] == a_id, books))


def get_book_ids():
    return [book['id'] for book in books]


def get_book_names():
    return [book['name'] for book in books]


def get_author_ids():
    return [author['id'] for author in authors]


def get_author_names():
    return [author['name'] for author in authors]


def generate_book_id():
    return reduce(lambda x, y: max(x, y), get_book_ids()) + 1


def generate_author_id():
    return reduce(lambda x, y: max(x, y), get_author_ids()) + 1


def create_book(b_name, b_aid):
    return {'id': generate_book_id(), 'name': b_name, 'authorId': b_aid}


def create_author(a_name):
    return {'id': generate_author_id(), 'name': a_name}


def append_book(book):
    books.append(book)


def append_author(author):
    authors.append(author)


def remove_book(book):
    books.remove(book)


def remove_author(author):
    authors.remove(author)
