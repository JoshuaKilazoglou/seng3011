from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask(__name__)

access_token = '2019883274951221|1c9281343bdcde168cdad00e354fd2aa'

@app.route('/')
def hello_world():
    return render_template("index.html")

# example: http://localhost:5000/api/v0.1/page?company=woolworths&fields=id,name,fan_count,website
@app.route('/api/v0.1/page', methods=['GET'])
def get_page():
    company = request.args.get('company')
    fields = request.args.get('fields')
    params = {'fields' : fields, 'access_token' : access_token}
    print(params)
    response = requests.get(f'https://graph.facebook.com/v2.11/{company}', params)
    return (response.text, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run()
