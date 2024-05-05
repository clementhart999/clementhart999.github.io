from flask import Flask, render_template
from pymongo import MongoClient
import os

app = Flask('app')
app.config['SECRET_KEY'] = os.getenv('CONFIG_KEY')

client = MongoClient("localhost", 27017)

db = client.Users

print(db)

@app.route('/')
def home():
    return render_template('index.html')

app.run(host='0.0.0.0', port=8080)