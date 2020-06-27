from graphene import Schema, ObjectType, String, List, Int, Field, Mutation, Boolean
from data.dummy_data import *

"""
Python Graphene Documentation:
https://docs.graphene-python.org/en/latest/quickstart/
"""

#
# GraphQL Adapters for dummy data
# Note: to solve circular dependencies use the construct lambda: MyObjectType (ok even if defined below)
#


class Book(ObjectType):
    """
    This represents a book written by an author.
    """
    id = Field(Int, required=True,
               description="The book unique identifier.")
    name = Field(String, required=True,
                 description="The book title.")
    authorId = Field(Int, required=True,
                     description="The author's unique identifier.")
    author = Field(lambda: Author,
                   description="The author's details.")

    def resolve_author(root, info):
        return get_author_from_id(root['authorId'])


class Author(ObjectType):
    """
    This represents an author of a book.
    """
    id = Field(Int, required=True,
               description="The author unique identifier.")
    name = Field(String, required=True,
                 description="The author name.")
    books = Field(List(lambda: Book),
                  description="All of the author's books.")

    def resolve_books(root, info):
        return get_books_from_author_id(root['id'])


#
# Query for dummy data
#


class Query(ObjectType):
    """
    Some GraphQL endpoints to play around with dummy data.
    """
    books = Field(List(Book),
                  description="Query the archived books.")
    authors = Field(List(Author),
                    description="Query the archived authors.")
    book = Field(Book, id=Int(description="The book unique identifier.", required=True),
                 description="Get a single book data.")
    author = Field(Author, id=Int(description="The author unique identifier.", required=True),
                   description="Get a single author data.")

    def resolve_books(root, info):
        return books

    def resolve_authors(root, info):
        return authors

    def resolve_book(root, info, id):
        return get_book_from_id(id)

    def resolve_author(root, info, id):
        return get_author_from_id(id)


#
# Mutations for dummy data
# Note: input fields are injected in the transformation fn's parameters
#       output fields must be set in the transformation fn
#

class AddBook(Mutation):
    """
    Add a new book.
    """
    # input fields
    class Arguments:
        name = String(description="The new book title.", required=True)
        authorId = Int(description="The new book author's unique identifier.", required=True)

    # output fields
    book = Field(lambda: Book,
                 description="The newly created book.")
    success = Field(Boolean,
                    description="Whether the mutation succeeded.")

    # transformation
    def mutate(root, info, name, authorId):
        book = None
        success = name not in get_book_names() and authorId in get_author_ids()

        if success:
            new_book = create_book(name, authorId)
            append_book(new_book)
            book = Book(**new_book)

        return AddBook(book=book, success=success)


class AddAuthor(Mutation):
    """
    Add a new author.
    """
    # input fields
    class Arguments:
        name = String(description="The new author name.", required=True)

    # output fields
    author = Field(lambda: Author,
                   description="The newly created author.")
    success = Field(Boolean,
                    description="Whether the mutation succeeded.")

    # transformation
    def mutate(root, info, name):
        author = None
        success = name not in get_author_names()

        if success:
            new_author = create_author(name)
            append_author(new_author)
            author = Author(**new_author)

        return AddAuthor(author=author, success=success)


class EditBook(Mutation):
    """
    Edit an existing book.
    """
    # input fields
    class Arguments:
        id = Int(description="The id of the book to edit.", required=True)
        name = String(description="The new book title.")
        authorId = Int(description="The new book author's unique identifier.")

    # output fields
    book = Field(lambda: Book,
                 description="The edited book.")
    success = Field(Boolean,
                    description="Whether the mutation succeeded.")

    # transformation
    def mutate(root, info, id, **kwargs):
        # this is how to handle optional arguments
        name = kwargs.get('name', None)
        authorId = kwargs.get('authorId', None)

        book = None
        existing_book = id in get_book_ids()
        valid_name = bool(name) and name not in get_book_names()
        valid_author_id = bool(authorId) and authorId in get_author_ids()
        success = existing_book and (valid_name or valid_author_id)

        if success:
            selected_book = get_book_from_id(id)
            remove_book(selected_book)
            selected_book['name'] = name if bool(name) else selected_book['name']
            selected_book['authorId'] = authorId if bool(authorId) else selected_book['name']
            append_book(selected_book)
            book = Book(**selected_book)
        return EditBook(book=book, success=success)


class EditAuthor(Mutation):
    """
    Edit an existing author.
    """
    # input fields
    class Arguments:
        id = Int(description="The id of the author to edit.", required=True)
        name = String(description="The new author name.")

    # output fields
    author = Field(lambda: Author,
                   description="The edited author.")
    success = Field(Boolean,
                    description="Whether the mutation succeeded.")

    # transformation
    def mutate(root, info, id, **kwargs):
        # this is how to handle optional arguments
        name = kwargs.get('name', None)

        author = None
        existing_author = id in get_author_ids()
        valid_name = bool(name) and name not in get_author_names()
        success = existing_author and valid_name

        if success:
            selected_author = get_author_from_id(id)
            remove_author(selected_author)
            selected_author['name'] = name if bool(name) else selected_author['name']
            append_author(selected_author)
            author = Author(**selected_author)
        return EditAuthor(author=author, success=success)


class DeleteBook(Mutation):
    """
    Delete an existing book.
    """
    # input fields
    class Arguments:
        id = Int(description="The id of the book to delete.", required=True)

    # output fields
    success = Field(Boolean,
                    description="Whether the mutation succeeded.")

    # transformation
    def mutate(root, info, id):
        success = id in get_book_ids()

        if success:
            selected_book = get_book_from_id(id)
            remove_book(selected_book)

        return DeleteBook(success=success)


class DeleteAuthor(Mutation):
    """
    Delete an existing author.
    """
    # input fields
    class Arguments:
        id = Int(description="The id of the author to delete.", required=True)

    # output fields
    success = Field(Boolean,
                    description="Whether the mutation succeeded.")

    # transformation
    def mutate(root, info, id):
        success = id in get_author_ids()
        if success:
            selected_author = get_author_from_id(id)
            remove_author(selected_author)
        return DeleteAuthor(success=success)


class Mutations(ObjectType):
    """
    Some GraphQL mutations to play around with dummy data.
    """
    addBook = AddBook.Field()
    addAuthor = AddAuthor.Field()
    editBook = EditBook.Field()
    editAuthor = EditAuthor.Field()
    deleteBook = DeleteBook.Field()
    deleteAuthor = DeleteAuthor.Field()


#
# Schema for dummy data
#


def get_schema():
    return Schema(query=Query, mutation=Mutations)
