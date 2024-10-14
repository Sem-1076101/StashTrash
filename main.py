from flask import Flask, session, render_template, request, url_for, flash, redirect

app = Flask(__name__)
DATABASEFILE = 'database/database.db'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
