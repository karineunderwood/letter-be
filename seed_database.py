"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
import model
import server



# use this seed_database.py to re-create my database

os.system("dropdb letters")
os.system("createdb letters")
# after that connect to the database and call db.create_all()

model.connect_to_db(server.app)
model.db.create_all()