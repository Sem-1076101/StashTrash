from flask import Flask, session, render_template, request, url_for, flash, redirect

app = Flask(__name__)
DATABASEFILE = 'database/database.db'

@app.route('/')
def home():
    return render_template('templates/home.html')