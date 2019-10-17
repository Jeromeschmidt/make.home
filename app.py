from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime
import random
from flask import Flask, render_template, request, redirect, url_for

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/MS_staff')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
MS_staff = db.MS_staff

app = Flask(__name__)

@app.route('/')
def index():
    """Show log in screen."""
    names = list()
    a = random.randrange(MS_staff.count())
    b = random.randrange(MS_staff.count())
    c = random.randrange(MS_staff.count())
    while((a == b) or (b == c) or (c == a)):
        a = random.randrange(MS_staff.count())
        b = random.randrange(MS_staff.count())
        c = random.randrange(MS_staff.count())
    person1=MS_staff.find()[a]
    person2=MS_staff.find()[b]
    person3=MS_staff.find()[c]
    names.append(person1["name"])
    names.append(person2["name"])
    names.append(person3["name"])
    random.shuffle(names)
    return render_template('index.html', person1=person1, names=names)

@app.route('/index2/<person_id>')
def index2(person_id):
    """Show log in screen."""
    person = MS_staff.find_one({'_id': ObjectId(person_id)})
    return render_template('index2.html', person=person)

def correct():
    print("!@!!!!!!!")

#owner landing page
@app.route('/admin')
def admin():
    """takes user to owner landing page"""
    return render_template('admin.html', MS_staff=MS_staff.find())

#creates a new item
@app.route('/person', methods=['POST'])
def person_submit():
    """Submit a new person."""
    person = {
        'name': request.form.get('name'),
        'bio': request.form.get('bio'),
        'image': request.form.get('image'),
        'created_at': datetime.now(),
    }
    person_id = MS_staff.insert_one(person).inserted_id
    return redirect(url_for('admin'))

#adds a new item
@app.route('/admin/add_person')
def add_person():
    """Create a new item."""
    return render_template('new_person.html', person={}, title='New person')

#lets the owner edit an item
@app.route('/admin/<person_id>/edit', methods=['POST'])
def edit_person(person_id):
    """edit an item."""
    person = MS_staff.find_one({'_id': ObjectId(person_id)})
    return render_template('edit_person.html', person=person, title='edit person')

#updates an edited item
@app.route('/admin/<person_id>', methods=['POST'])
def person_update(person_id):
    """Submit an edited person."""
    updated_person = {
        'name': request.form.get('name'),
        'bio': request.form.get('bio'),
        'image': request.form.get('image')
    }
    MS_staff.update_one(
        {'_id': ObjectId(person_id)},
        {'$set': updated_person})
    return render_template('admin.html', MS_staff=MS_staff.find())

#lets owner delete an item
@app.route('/admin/<person_id>/delete', methods=['POST'])
def person_delete(person_id):
    """Delete one person."""
    MS_staff.delete_one({'_id': ObjectId(person_id)})
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
