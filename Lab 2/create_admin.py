from app import app, db
from models import User

def create_admin():
    with app.app_context():
        admin_exists = User.query.filter_by(is_admin=True).first()
        if admin_exists:
            print('Admin user already exists.')
            return
        
        username = 'admin'
        email = 'admin@example.com'
        password = 'adminpassword'
        
        new_admin = User(username=username, email=email, is_admin=True)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()
        print('Admin user created successfully!')

if __name__ == '__main__':
    create_admin()
