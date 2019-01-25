#!/usr/bin/env python
from redis import Redis
import time
from functools import update_wrapper
from flask import request, g
from flask import Flask, jsonify, render_template
from redis import Redis

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import json

app = Flask(__name__)

# fake database
fcategory = {'name': 'soccer', 'id': '1'}
fcategories = [{'name': 'soccer', 'id': '1'}, {'name': 'Basketball', 'id': '2'}, {'name': 'Baseball', 'id': '3'}]
fitem = {'name': 'ball', 'description': 'this is a ball lul', 'id': '1'}
fitems = [{'name': 'ball', 'description': 'this is a ball lul', 'id': '1'},
         {'name': 'goggles', 'description': 'this is a goggle lul lul', 'id': '2'},
         {'name': 'snowboard', 'description': 'this is a snowboard lul lul lul', 'id': '3'}]



@app.route('/')
@app.route('/catalog')
def showCatalogs():
    return render_template('all_catalog.html', categories=fcategories)


# leads to edit item if logged
# leads to delete item if logged
@app.route('/catalog/<path:category>/items')
def showCategoryItems(category):
    return render_template('show_category_items.html', categories=fcategories, current_category=category, items=fitems)


# leads to edit item if logged
# leads to delete item if logged
@app.route('/catalog/<path:category>/<path:item>')
def showItem(category, item):
    return render_template('show_item.html', categories=fcategories, current_item=item, item=fitem)


# needs to be loged
@app.route('/catalog/<path:item>/edit')
def editItem(item):
    return render_template('edit_item.html', categories=fcategories, current_item=item, item=fitem)


# needs to be loged
@app.route('/catalog/<path:item>/delete')
def deleteItem(item):
    return render_template('delete_item.html', categories=fcategories, current_item=item, item=fitem)


# needs to be loged
@app.route('/catalog/add')
def addItem():
    return render_template('add_item.html', categories=fcategories)


@app.route('/catalog.json')
def showJson():
    return "this is the json of all the catalog items"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
