from flask import Flask, request, redirect, render_template, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'books.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author) VALUES (?, ?)',
                     (title, author))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit_book(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn.execute('UPDATE books SET title = ?, author = ? WHERE id = ?',
                     (title, author, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit_book.html', book=book)

@app.route('/<int:id>/delete', methods=('POST',))
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


