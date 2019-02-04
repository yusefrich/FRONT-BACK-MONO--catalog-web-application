#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images'
                     '/2671170543'
                     '/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# create categories
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

# creating items
item1 = Item(user_id=1, name="ball", description="Colored soccer ball",
             category=category1)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="football boots",
             description="New pink football boots",
             category=category1)

session.add(item1)
session.commit()

category2 = Category(name="Basketball")
session.add(category2)
session.commit()

# creating items
item1 = Item(user_id=1, name="basketball", description="Brown basketball",
             category=category2)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="Basket",
             description="big red retractable basket",
             category=category2)

session.add(item1)
session.commit()

category3 = Category(name="Baseball")
session.add(category3)
session.commit()

# creating items
item1 = Item(user_id=1, name="Baseball ball",
             description="New and bright Baseball ball",
             category=category3)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="baseball bat",
             description="big red baseball bat with a team sticker",
             category=category3)

session.add(item1)
session.commit()

category4 = Category(name="Frisbee")
session.add(category4)
session.commit()

# creating items
item1 = Item(user_id=1, name="Frisbee disk",
             description="New and bright Frisbee disk",
             category=category4)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="Frisbee uniform",
             description="The complete outfit to play frisbee",
             category=category4)

session.add(item1)
session.commit()

category5 = Category(name="Snowboarding")
session.add(category5)
session.commit()

# creating items
item1 = Item(user_id=1, name="Snowboard",
             description="essential to play snowboard",
             category=category5)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="Snowboard goggles",
             description="essential safety gear",
             category=category5)

session.add(item1)
session.commit()

category6 = Category(name="Rock Climbing")
session.add(category6)
session.commit()

# creating items
item1 = Item(user_id=1, name="Rock Climbing belt",
             description="belt used to rock climbing ",
             category=category6)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="Rock Climbing shoes",
             description="essential for climbing",
             category=category6)

session.add(item1)
session.commit()

category7 = Category(name="Foosball")
session.add(category7)
session.commit()

# creating items
item1 = Item(user_id=1, name="Foosball table",
             description="Foosball table for playing ",
             category=category7)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="Foosball mini balls",
             description="Pair these fun sports balls with other novelty toys",
             category=category7)

session.add(item1)
session.commit()

category8 = Category(name="Skating")
session.add(category8)
session.commit()

# creating items
item1 = Item(user_id=1, name="Skate",
             description="pro skates to play the sport ",
             category=category8)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="bearing",
             description="used on the wells for beater performance",
             category=category8)

session.add(item1)
session.commit()

category9 = Category(name="Hockey")
session.add(category9)
session.commit()

# creating items
item1 = Item(user_id=1, name="Hockey bat",
             description="bat used for players to play the game ",
             category=category9)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="Hockey ball",
             description="ball optimized for Hockey",
             category=category9)

session.add(item1)
session.commit()

category10 = Category(name="Other")
session.add(category10)
session.commit()

# creating items
item1 = Item(user_id=1, name="swimming goggles",
             description="used in swimming ",
             category=category10)

session.add(item1)
session.commit()

item1 = Item(user_id=1, name="Running shoes",
             description="running requires great shoes",
             category=category10)

session.add(item1)
session.commit()

print("added all items")
