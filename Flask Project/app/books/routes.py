from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Book

books_bp = Blueprint('books', __name__)

@books_bp.route('/dashboard')
@login_required
def dashboard():
    books = Book.query.filter_by(owner=current_user).all()
    return render_template('books/dashboard.html', books=books)

@books_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        image = request.files['image'].read() if 'image' in request.files else None
        
        new_book = Book(title=title, author=author, image=image, owner=current_user)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.dashboard'))
    return render_template('books/add_book.html')

@books_bp.route('/delete/<int:book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner != current_user and not current_user.is_admin:
        flash('You are not authorized to delete this book.', 'danger')
        return redirect(url_for('books.dashboard'))
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully.', 'success')
    return redirect(url_for('books.dashboard'))
