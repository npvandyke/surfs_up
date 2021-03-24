# Import dependency 
from flask import Flask
# Create a new Flask app instance 
app = Flask(__name__)
# Define the starting point (root) of the first route
@app.route('/')
def hello_world():
    return 'Hello world'

