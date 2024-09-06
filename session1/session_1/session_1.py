from flask import Flask, redirect, url_for, render_template
from flask import request, session
from datetime import timedelta

app = Flask(__name__, static_folder='static')
app.secret_key ='12345'
app.permanent_session_lifetime = timedelta(minutes= 30)
students = [{'id': 1, 'name': 'Ahmed', 'age': 20},{'id': 2, 'name': 'sara', 'age': 25}, {'id': 3, 'name': 'Mahmoud', 'age': 22}]

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
        session ['username'] = username
        session['password'] = password
        return redirect(url_for('profile'))
    else:
        return render_template('login.html')
    
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if 'username' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        session ['username'] = username
        session['password'] = password
        
        if password == confirm_password:
            # add user to the database
            return redirect(url_for('profile'))
        else:
            return "Passwords do not match"
    
    return render_template('sign_up.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('password', None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        password = session['password']
        # return f"Welcome, {username}! Your password is {password}" 
        return render_template('profile.html', username = username, password = password)
    else:
        return redirect(url_for('login'))

@app.route('/student/info')
def show_info():
    name = 'Ahmed'
    age = 25
    id = 0
    
    if id == 0:
        # return redirect("http://127.0.0.1:5000/home")
        return redirect(url_for('home'))
    else:
        return f"Hello, {name}, your age is {age}, and your id is {id}"

if __name__ == '__main__':
    app.run(debug=True, port = 5000)
