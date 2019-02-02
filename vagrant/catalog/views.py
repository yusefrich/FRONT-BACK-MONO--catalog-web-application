#!/usr/bin/env python
import random
import string

from flask import Flask, jsonify, render_template, redirect, url_for, flash
from flask import request
from flask import session as login_session
from models import Base, Category, Item, User
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, scoped_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('app_secrets/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Menu Application"


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine))

latestItems = []

# gconnect route
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('app_secrets/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1 class="text-light">Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 150px; height: 150px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', client_id=CLIENT_ID, STATE=state)


@app.route('/')
@app.route('/catalog')
def showCatalogs():
    categories = session.query(Category).order_by(asc(Category.id))
    return render_template('all_catalog.html', categories=categories, latest_items=latestItems)


# leads to edit item if logged
# leads to delete item if logged
@app.route('/catalog/<path:category>/items')
def showCategoryItems(category):
    categories = session.query(Category).order_by(asc(Category.id))
    category = session.query(Category).filter_by(name=category).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('show_category_items.html', categories=categories, current_category=category, items=items)


# leads to edit item if logged
# leads to delete item if logged
@app.route('/catalog/<path:category>/<path:item>')
def showItem(category, item):
    categories = session.query(Category).order_by(asc(Category.id))
    current_item = session.query(Item).filter_by(name=item).one()
    viewedItem = { "name": current_item.name, "category": current_item.category.name}
    latestItems.append(viewedItem)
    if len(latestItems) > 3:
        latestItems.pop(0)
    return render_template('show_item.html', categories=categories, current_item=current_item)


# needs to be loged
@app.route('/catalog/<path:item>/edit', methods=['GET', 'POST'])
def editItem(item):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).order_by(asc(Category.id))
    editedItem = session.query(Item).filter_by(name=item).one()
    if request.method == 'POST':

        # check if item already exists
        try:
            itemAlreadyExists = session.query(Item).filter_by(name=request.form['name']).one()
        except:
            itemAlreadyExists = None
        if itemAlreadyExists:
            flash("this item name already exists")
            return redirect(url_for('editItem', item=editedItem.name))
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['category']:
            newCategory = session.query(Category).filter_by(name=request.form['category']).one()
            editedItem.category = newCategory
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash("Item successfully edited!!")
        return redirect(url_for('showCategoryItems', category=editedItem.category.name))
    else:
        return render_template('edit_item.html', categories=categories, current_item=editedItem)


# needs to be loged
@app.route('/catalog/<path:item>/delete', methods=['GET', 'POST'])
def deleteItem(item):
    if 'username' not in login_session:
        return redirect('/login')

    categories = session.query(Category).order_by(asc(Category.id))
    itemToDelete = session.query(Item).filter_by(name=item).one()
    category = session.query(Category).filter_by(name=itemToDelete.category.name).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item successfully deleted!!")
        return redirect(url_for('showCategoryItems', category=category.name))
    else:
        return render_template('delete_item.html', categories=categories, current_item=itemToDelete)


# needs to be loged
@app.route('/catalog/add', methods=['GET', 'POST'])
def addItem():
    if 'username' not in login_session:
        return redirect('/login')

    categories = session.query(Category).order_by(asc(Category.id))
    newItemDescription = "Item has no description"
    if request.method == 'POST':
        try:
            itemAlreadyExists = session.query(Item).filter_by(name=request.form['name']).one()
        except:
            itemAlreadyExists = None

        if itemAlreadyExists:
            flash("this item name already exists")
            return redirect(url_for('addItem'))
        newItemName = request.form['name']
        newItemCategory = session.query(Category).filter_by(name=request.form['category']).one()
        if request.form['description']:
            newItemDescription = request.form['description']
        newItem = Item(name=newItemName, category=newItemCategory, description=newItemDescription, user_id=getUserID(login_session['email']) )
        session.add(newItem)
        session.commit()
        flash("New Item Created!!")
        return redirect(url_for('showCategoryItems', category=newItemCategory.name))
    else:
        return render_template('add_item.html', categories=categories)


@app.route('/catalog.json')
def showJson():
    categories = session.query(Category).order_by(asc(Category.id))
    category_dict = [c.serialize for c in categories]
    for c in range(len(category_dict)):
        items = [i.serialize for i in session.query(Item) \
            .filter_by(category_id=category_dict[c]["id"]).all()]
        if items:
            category_dict[c]["Item"] = items

    return jsonify(categories=category_dict)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
