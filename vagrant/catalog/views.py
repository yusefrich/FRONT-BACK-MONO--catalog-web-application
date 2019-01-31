#!/usr/bin/env python
from redis import Redis
import time
from functools import update_wrapper
from flask import request, g
from flask import Flask, jsonify, render_template, redirect, url_for, flash
from models import Base, Category, Item, User
from redis import Redis

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine, asc

import json

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine))


@app.route('/')
@app.route('/catalog')
def showCatalogs():
    categories = session.query(Category).order_by(asc(Category.id))
    return render_template('all_catalog.html', categories=categories)


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
    return render_template('show_item.html', categories=categories, current_item=current_item)


# needs to be loged
@app.route('/catalog/<path:item>/edit', methods=['GET', 'POST'])
def editItem(item):
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
        newItem = Item(name=newItemName, category=newItemCategory, description=newItemDescription)
        session.add(newItem)
        session.commit()
        flash("New Item Created!!")
        return redirect(url_for('showCategoryItems', category=newItemCategory.name))
    else:
        return render_template('add_item.html', categories=categories)


@app.route('/catalog.json')
def showJson():
    return "this is the json of all the catalog items"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
