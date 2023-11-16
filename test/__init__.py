import os

os.remove("instance/temp_test.sqlite3")
from app import app

app.config['TESTING'] = True
client = app.test_client()
