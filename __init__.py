from flask import Flask
from flask import render_template
from flask import request
from flask_restful import Api
from PageDataController import PageDataController

app = Flask(__name__)
api = Api(app)

apiVersion = 'v1'
access_token = '2019883274951221|1c9281343bdcde168cdad00e354fd2aa'

# create endpoints like this with flask_restful
api.add_resource(PageDataController, '/api/' + apiVersion + '/PageData')

@app.route('/')
def home():
    return render_template("index.html")

# old way of creating endpoints
# example: http://localhost:5000/api/v0.1/page?company=woolworths&fields=id,name,fan_count,website
@app.route('/api/v0.1/page', methods=['GET'])
def get_page():
    company = request.args.get('company')
    fields = request.args.get('fields')
    params = {'fields' : fields, 'access_token' : access_token}
    print(params)
    response = requests.get('https://graph.facebook.com/v2.11/' + company, params)
    return (response.text, response.status_code, response.headers.items())
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
if __name__ == '__main__':
    app.run()
