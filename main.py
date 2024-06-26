from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), default="user")

    requests = db.relationship('Request', backref='user_relationship', lazy=True)

# Define the Genre model
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    books = db.relationship('Book', back_populates='genre')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(500), nullable=True)

    requests = db.relationship('Request', backref='books_relationship', lazy=True)
    genre = db.relationship('Genre', back_populates='books')

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, default=datetime.utcnow) 
    status = db.Column(db.String(20), default='Pending', nullable=False)
    user = db.relationship('User', backref='requests_user_relationship', lazy=True)
    book = db.relationship('Book', backref='requests__books_relationship', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'status': self.status,
            'issue_date': self.issue_date.isoformat(),
            'request_date': self.return_date.isoformat(),
        }
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Feedback {self.id} - Book {self.book_id}>'

@app.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    email = req_data.get('email')
    password = req_data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if email == 'admin@gmail.com' and password == 'admin':
        return jsonify({
            "message": "Login successful",
            "email": email,
            "role": "librarian"
        })

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404

    if user.password != password:
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({
        "message": "Login successful",
        "email": email,
        "userId": user.id,
        "role": user.role
    })

@app.route('/register', methods=['POST'])
def register():
    req_data = request.get_json()
    email = req_data.get('email')
    password = req_data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "User already exists"}), 409

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"})

@app.route('/add-genre', methods=['POST'])
def add_genre():
    req_data = request.get_json()
    title = req_data.get('title')
    description = req_data.get('description')
    image_url = req_data.get('image_url', '')  # Optional field

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    if Genre.query.filter_by(title=title).first():
        return jsonify({"error": "Genre already exists"}), 409

    new_genre = Genre(title=title, description=description, image=image_url)
    db.session.add(new_genre)
    db.session.commit()
    
    return jsonify({"message": "Genre added successfully", "genre": {"id": new_genre.id, "title": new_genre.title, "description": new_genre.description, "image_url": new_genre.image, "date_created": new_genre.date_created}})

@app.route('/genres', methods=['GET'])
def get_genres():
    genres = Genre.query.all()
    genres_list = [{"id": genre.id, "title": genre.title, "description": genre.description, "image_url": genre.image, "date_created": genre.date_created} for genre in genres]
    return jsonify({"genres": genres_list})

@app.route('/edit-genre/<int:genre_id>', methods=['PUT'])
def edit_genre(genre_id):
    req_data = request.get_json()
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({"error": "Genre not found"}), 404

    title = req_data.get('title')
    description = req_data.get('description')
    image_url = req_data.get('image_url')

    if title:
        genre.title = title
    if description:
        genre.description = description
    if image_url is not None:
        genre.image = image_url

    db.session.commit()
    return jsonify({"message": "Genre updated successfully", "genre": {"id": genre.id, "title": genre.title, "description": genre.description, "image_url": genre.image, "date_created": genre.date_created}})

@app.route('/delete-genre/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({"error": "Genre not found"}), 404

    db.session.delete(genre)
    db.session.commit()
    return jsonify({"message": "Genre deleted successfully"})

# Route to add a new book
@app.route('/add-book', methods=['POST'])
def add_book():
    req_data = request.get_json()
    title = req_data.get('title')
    author = req_data.get('author')
    genre_id = req_data.get('genre_id')
    description = req_data.get('description', '')

    if not title or not author or not genre_id:
        return jsonify({"error": "Title, author, and genre ID are required"}), 400

    new_book = Book(title=title, author=author, genre_id=genre_id, description=description)
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({"message": "Book added successfully", "book": {"id": new_book.id, "title": new_book.title, "author": new_book.author, "description": new_book.description, "date_created": new_book.date_created}})

@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'date_created': book.date_created
        }), 200
    else:
        return jsonify({'message': 'Book not found'}), 404
    
# Route to fetch all books by genre
@app.route('/genres/<int:genre_id>/books', methods=['GET'])
def get_books_by_genre(genre_id):
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({"error": "Genre not found"}), 404

    books = Book.query.filter_by(genre_id=genre_id).all()
    return jsonify({"books": [{"id": book.id, "title": book.title, "author": book.author, "description": book.description, "date_created": book.date_created} for book in books]})

# Route to edit a book
@app.route('/edit-book/<int:book_id>', methods=['PUT'])
def edit_book(book_id):
    req_data = request.get_json()
    book = Book.query.get(book_id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    book.title = req_data.get('title', book.title)
    book.author = req_data.get('author', book.author)
    book.description = req_data.get('description', book.description)
    book.genre_id = req_data.get('genre_id', book.genre_id)

    db.session.commit()
    return jsonify({"message": "Book updated successfully", "book": {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "genre_id": book.genre_id
    }})

# Route to delete a book
@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})

@app.route('/request-book', methods=['POST'])
def request_book():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    # Fetch user to ensure it exists
    user = User.query.get(user_id)
    if not user:
        print("User not found")
        return jsonify({'error': 'User not found'}), 404

    # Fetch book to ensure it exists
    book = Book.query.get(book_id)
    if not book:
        print("Book not found")
        return jsonify({'error': 'Book not found'}), 404

    new_request = Request(
        user_id=user_id,
        book_id=book_id,
        status='pending',
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Request created successfully'}), 201

@app.route('/users/<int:user_id>/books', methods=['GET'])
def get_books_by_user(user_id):
    # Query books associated with the user_id
    accepted_books = Request.query.filter_by(user_id=user_id, status = "accepted").all()
    
    books = [(request.book) for request in accepted_books]
    # Prepare JSON response
    books_list = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre_id': book.genre_id,
        'date_created': book.date_created.isoformat(),
        'description': book.description
    } for book in books]

    return jsonify({'books': books_list})

@app.route('/requests/all', methods=['GET'])
def get_all_requests():
    requests = Request.query.all()
    request_list = [{
        'id': req.id,
        'user_id': req.user_id,
        'user_email': User.query.get(req.user_id).email,
        'book_id': req.book_id,
        'issue_date': req.issue_date,
        'book_title': Book.query.get(req.book_id).title,
        'status': req.status,
    } for req in requests]
    return jsonify({'requests': request_list})

@app.route('/requests', methods=['GET'])
def get_requests():
    requests = Request.query.filter_by(status = "pending")
    request_list = [{
        'id': req.id,
        'user_name': User.query.get(req.user_id).email,
        'book_title': Book.query.get(req.book_id).title,
        'status': req.status,
    } for req in requests]
    return jsonify({'requests': request_list})

@app.route('/requests-for-all-books', methods=['GET'])
def get_requests_for_all_books():
    requests_all = Request.query.filter_by(status = "accepted").all()
    request_list_all_books = [{
        'id': req.id,
        'user_id': req.user_id,
        'book_id': req.book_id,
        'status': req.status,
        'book_title': req.book.title,
        'book_author': req.book.author,
        'book_description': req.book.description
    } for req in requests_all]
    return jsonify({'requests': request_list_all_books})

@app.route('/requests/<int:request_id>/accept', methods=['POST'])
def accept_request(request_id):
    req = Request.query.get(request_id)
    if req:
        req.status = 'accepted'
        req.issue_date = datetime.utcnow()
        db.session.commit()
        return '', 204
    return '', 404

@app.route('/requests/<int:request_id>/reject', methods=['POST'])
def reject_request(request_id):
    req = Request.query.get(request_id)
    if req:
        req.status = 'rejected'
        db.session.delete(req)
        db.session.commit()
        return '', 204
    return '', 404

@app.route('/return-book/<int:book_id>', methods=['POST'])
def return_book(book_id):
    user_id = request.json.get('user_id')
    request_record = Request.query.filter_by(book_id=book_id, status='accepted').first()
    
    if request_record:
        db.session.delete(request_record)
        db.session.commit()
        return jsonify({'message': 'Book returned successfully'}), 200
    else:
        return jsonify({'message': 'Book not found or not allocated to user'}), 404

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    feedback_text = data.get('feedback_text')

    if not user_id or not book_id or not feedback_text:
        return jsonify({'error': 'User ID, Book ID, and feedback text are required'}), 400

    user = User.query.get(user_id)
    book = Book.query.get(book_id)
    
    if not user or not book:
        return jsonify({'error': 'Invalid user or book ID'}), 404

    feedback = Feedback(user_id=user_id, book_id=book_id, feedback_text=feedback_text)
    db.session.add(feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback submitted successfully'}), 201

@app.route('/feedback/<int:book_id>', methods=['GET'])
def get_feedback(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    feedbacks = Feedback.query.filter_by(book_id=book_id).all()
    feedback_list = [{
        'id': feedback.id,
        'user_id': feedback.user_id,
        'feedback_text': feedback.feedback_text,
        'date_created': feedback.date_created.isoformat()
    } for feedback in feedbacks]

    return jsonify({'feedbacks': feedback_list})

@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'books': []})
    
    # Assuming you have a Book model with title and author fields
    books = Book.query.filter((Book.title.ilike(f'%{query}%')) | (Book.author.ilike(f'%{query}%'))).all()
    
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
    
    return jsonify({'books': book_list})

if __name__ == '__main__':
    # Create the database and tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
