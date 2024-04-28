from flask import Flask, render_template
from pymongo import MongoClient

app = Flask('app')

@app.route('/')
def home():
    return render_template('index.html')

app.run(host='0.0.0.0', port=8080)