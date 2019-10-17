from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/MS_staff')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
MS_staff = db.MS_staff

app = Flask(__name__)

@app.route('/')
def index():
    """Show log in screen."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
