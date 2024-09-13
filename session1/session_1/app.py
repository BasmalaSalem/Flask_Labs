from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.secret_key = '12345'
app.permanent_session_lifetime = timedelta(minutes=30)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password

# Sample student data
students = [{'id': 1, 'name': 'Ahmed', 'age': 20}, {'id': 2, 'name': 'Sara', 'age': 25}, {'id': 3, 'name': 'Mahmoud', 'age': 22}]

@app.route('/')
def students_list():
    return render_template('index.html', students=students)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/search/<int:id>')
@app.route('/search', methods=['GET'])
def search():
    student_id = request.args.get('id')
    if student_id:
        student_id = int(student_id)
        student = next((student for student in students if student['id'] == student_id), None)
        return render_template('search_result.html', student=student)
    return redirect(url_for('home'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        session.permanent = True
        username = request.form.get('username')
        password = request.form.get('password')
        # Find user in the database
        found_user = User.query.filter_by(username=username).first()
        if found_user and check_password_hash(found_user.password, password):
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if 'username' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password == confirm_password:
            found_user = User.query.filter_by(username=username).first()
            if found_user:
                flash("Username already exists", "danger")
                return redirect(url_for('sign_up'))
            else:
                new_user = User(username=username, password=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                flash("Account created successfully", "success")
                return redirect(url_for('login'))
        else:
            flash("Passwords do not match", "danger")
            return redirect(url_for('sign_up'))
    return render_template('sign_up.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out", "info")
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', username=username)
    else:
        flash("Please log in to view your profile", "warning")
        return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        flash("Please log in to edit your profile", "warning")
        return redirect(url_for('login'))
    
    current_user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if new_password and new_password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('edit_profile'))

        current_user.username = new_username or current_user.username
        if new_password:
            current_user.password = generate_password_hash(new_password)

        db.session.commit()
        session['username'] = current_user.username
        flash("Profile updated successfully", "success")
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=current_user)

@app.route('/delete_profile', methods=['POST', 'GET'])
def delete_profile():
    if 'username' not in session:
        flash("Please log in to delete your profile", "warning")
        return redirect(url_for('login'))

    current_user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        if current_user:
            db.session.delete(current_user)
            db.session.commit()
            
            session.pop('username', None)
            session.pop('password', None)
            
            flash("Profile deleted successfully", "success")
            return redirect(url_for('sign_up'))
        else:
            flash("User not found", "danger")
            return redirect(url_for('profile'))

    return render_template('delete_profile.html', user=current_user)


@app.route('/student/info')
def show_info():
    name = 'Ahmed'
    age = 25
    id = 0
    
    if id == 0:
        return redirect(url_for('home'))
    else:
        return f"Hello, {name}, your age is {age}, and your id is {id}"

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
