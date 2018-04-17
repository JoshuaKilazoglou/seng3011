from flask import Flask
from flask import render_template
from flask import request
import requests
from flask_restful import Api
import json

from PageDataController import PageDataController


app = Flask(__name__)
api = Api(app)

apiVersion = 'v1'

# create endpoints like this with flask_restful
api.add_resource(PageDataController, '/api/' + apiVersion + '/PageData')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/inputDocs')
def get_indocs():
    return render_template("indocs.html")

@app.route('/exampleDocs')
def get_exampledocs():
    return render_template("exampledocs.html")

@app.route('/outputDocs')
def get_outdocs():
    return render_template("outdocs.html")

@app.route('/version')
def get_version():
    return render_template("version.html")

@app.route('/gui' , methods=['POST'])
def gui():
    company = request.form.get('company')
    startdate = request.form.get('startdate')
    enddate = request.form.get('enddate')
   # description = request.form.get('description')
    url = 'http://seng3011laser.com/api/v1/PageData?company=' + company + '&startdate=' +startdate + '&enddate=' + enddate + "&fields=description,fan_count"

    # encode parameters in request url

    # send request, get response
    response = requests.get(url)




    return render_template("gui.html", company1 = response.json() )

if __name__ == '__main__':
    app.run()
