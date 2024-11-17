from flask import Flask, session, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from database.session import User,  db_session, Report ,PointsHistory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'een_zeer_geheime_en_unieke_sleutel'
curent_dir = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/trashtagger.db"

# DATABASEFILE = 'database/trashtagger.db'

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = db_session.query(User).all()
    print(users)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db_session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            print(f"User logged in: {user.id}")
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login', user_not_found=True))
    user_not_found = request.args.get('user_not_found')
    
    return render_template('login.html', logged_in='user_id' in session, user_not_found=user_not_found)

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if db_session.query(User).filter_by(email=email).first():
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        try:
            db_session.add(new_user)
            db_session.commit()
            session['user_id'] = new_user.id
            return redirect(url_for('home'))
        except Exception as e:
            print(f"Error during commit: {e}")
            db_session.rollback()
            return redirect(url_for('register'))

    return render_template('register.html', logged_in='user_id' in session)




@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
