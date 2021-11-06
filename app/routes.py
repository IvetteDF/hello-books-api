from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        title_query = request.args.get("title")
        if title_query:
            books = Book.query.filter_by(title=title_query)
        else:
            books = Book.query.all()

        books_response = []
        for book in books:
            books_response.append({
                "id" : book.id, 
                "title" : book.title,
                "description" : book.description
            })
        return jsonify(books_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title=request_body["title"], description=request_body["description"])

        # tells SQLAlchemy that there was a db interaction
        db.session.add(new_book)
        db.session.commit()

        return jsonify(new_book.to_dict()), 201

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id)
    # or if not book:
    if book is None:
        return make_response("", 404)

    if request.method == "GET":
        return {
            "id" : book.id,
            "title" : book.title,
            "description" : book.description
        }
    elif request.method == "PUT":
        form_data = request.get_json()

        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()

        return make_response(f"Book #{book.id} successfully updated")
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} successfully deleted")

@authors_bp.route("", methods=["GET", "POST"])
def handle_authors():
    if request.method == "GET":
        authors = Author.query_all()

        authors_response = []
        for author in authors:
            authors_response.append({
                "id" : author.id,
                "name" : author.name
            })
        return jsonify(authors_response)
        
    elif request.method == "POST":
        request_body = request.get_json()
        new_author = Author(name=request_body["name"])

        db.session.add(new_author)
        db.session.commit()

        return jsonify({
            "id" : new_author.id,
            "name" : new_author.name
        }), 201

@authors_bp.route("/<author_id>/books", methods=["GET", "POST"])
def handle_authors_books(author_id):
    author = Author.query.get(id=author_id)
    if author is None:
        return jsonify("Author not found"), 404

    if request.method == "POST":
        request_body = request.get_json()

        new_book = Book(
            title=request_body["title"],
            description=request_body["description"], 
            author=author
        )

        db.session.add(new_book)
        db.session.commit()

        return jsonify(f"Book {new_book.title} by {new_book.author}, successfully created"), 201

    elif request.method == "GET":
        books_response = []
        for book in author.books:
            books_response.append({
                "id" : book.id,
                "title" : book.title, 
                "description" : book.description
            })
        return jsonify(books_response)