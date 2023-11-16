import os

db_file = "instance/temp_test.sqlite3"
if os.path.isfile(db_file):
    os.remove(db_file)
from app import app

app.config['TESTING'] = True
client = app.test_client()
