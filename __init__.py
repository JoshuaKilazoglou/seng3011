from flask import Flask
from flask import render_template
from flask import request
import requests
from flask_restful import Api
from V1.PageDataControllerV1 import PageDataControllerV1
from V2.PageDataControllerV2 import PageDataControllerV2
from flask import redirect


app = Flask(__name__)
api = Api(app)

# create endpoints like this with flask_restful
api.add_resource(PageDataControllerV1, '/api/v1/PageData')
api.add_resource(PageDataControllerV2, '/api/v2/PageData')

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

    company = str.strip(request.form.get('company'))
    startdate = str.strip(request.form.get('startdate'))
    enddate = str.strip(request.form.get('enddate'))
   # description = request.form.get('description')
    url = 'http://seng3011laser.com/api/v1/PageData?company=' + company + '&startdate=' +startdate + '&enddate=' + enddate + "&fields=description,fan_count"
    print(request.form.get('fans'))

    # send request, get response
    response = requests.get(url)




    return render_template("gui.html", company1 = response.json() )

if __name__ == '__main__':
    app.run()
