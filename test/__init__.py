from app import app

app.config['TESTING'] = True
client = app.test_client()
