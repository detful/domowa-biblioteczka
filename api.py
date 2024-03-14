from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'books.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books_cursor = conn.execute('SELECT * FROM books')
    books = books_cursor.fetchall()
    conn.close()
    books_list = [dict(book) for book in books]
    return jsonify(books_list)

@app.route('/books', methods=['POST'])
def add_book():
    if request.method == 'POST':
        new_book = request.json
        title = new_book['title']
        author = new_book['author']
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book added successfully!'}), 201

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    conn.close()
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify(dict(book))

@app.route('/books/<int:id>', methods=['PUT'])
def edit_book(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()

    if book is None:
        conn.close()
        return jsonify({'message': 'Book not found'}), 404

    update_data = request.json
    title = update_data['title']
    author = update_data['author']

    conn.execute('UPDATE books SET title = ?, author = ? WHERE id = ?', (title, author, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book updated successfully'}), 200

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
