from flask import Flask
from flask import render_template
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/test', methods=['GET'])
def get_page():
    return requests.get("http://graph.facebook.com/v2.11/820882001277849?access_token=2019883274951221|1c9281343bdcde168cdad00e354fd2aa")


if __name__ == '__main__':
    app.run()
