from flask import Flask, url_for
from flask import render_template
from flask import request
import requests
import re
from flask import redirect
from flask_restful import Api
from V1.PageDataControllerV1 import PageDataControllerV1
from V2.PageDataControllerV2 import PageDataControllerV2
from aylienapiclient import textapi
import pygal
from datetime import date
from PoliticalWebsite import MainController

app = Flask(__name__)
api = Api(app)

client = textapi.Client("84fb5f8e", "42902aee45567b5e27375393a0ac4c70")


#  =================================================
#  == Political website endpoints registered here ==
#  =================================================

api.add_resource(MainController.Events, '/api/pw/Events')
api.add_resource(MainController.NewsArticles, '/api/pw/NewsArticles')
api.add_resource(MainController.GraphData, '/api/pw/GraphData')
api.add_resource(MainController.Sectors, '/api/pw/Sectors')
api.add_resource(MainController.PostSentiment, '/api/pw/PostSentiment')


#  ===============================================
#  == Old stuff below, shouldn't need to touch  ==
#  ===============================================


# create endpoints like this with flask_restful
api.add_resource(PageDataControllerV1, '/api/v1/PageData')
api.add_resource(PageDataControllerV2, '/api/v2/PageData')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/inputDocs')
def get_indocs():
    version = request.args.get('version')
    if version == None:
        return render_template("indocs.html")
    doc = "indocs" + version + ".html"
    print(doc)
    return render_template(doc)

@app.route('/exampleDocs')
def get_exampledocs():
    return render_template("exampledocs.html")

@app.route('/outputDocs')
def get_outdocs():
    version = request.args.get('version')
    if version == None:
        return render_template("outdocs.html")
    doc = "outdocs" + version + ".html"
    print(doc)
    return render_template(doc)


@app.route('/version')
def get_version():
    return render_template("version.html")

@app.route('/gui' , methods=['POST'])
def gui():
    error = 0
    companyE = ''
    startE = ''
    endE = ''

    #strip whitespace
    company = str.strip(request.form.get('company'))
    startdate = str.strip(request.form.get('startdate'))
    enddate = str.strip(request.form.get('enddate'))

    #check for errors in the params
    if not re.match('^[\-\_a-z0-9]+$', company):
        companyE = 'Invalid Company'
        error = 1
    if not re.match('[0-9]{4}\-[0-9]{2}\-[0-9]{2}T[0-9]{2}\:[0-9]{2}\:[0-9]{2}\.[0-9]{3}Z', startdate):
        startE = 'Incorrect start date format'
        error = 1
    if not re.match('[0-9]{4}\-[0-9]{2}\-[0-9]{2}T[0-9]{2}\:[0-9]{2}\:[0-9]{2}\.[0-9]{3}Z', enddate):
        endE = 'Incorrect end date format'
        error = 1

    if enddate <= startdate:
        endE = 'The end date must not be the same/before the start date'
        error = 1
    if error == 1:
        return render_template('index.html',companyError=companyE,startError=startE,endError=endE)

    fields = "&fields="
    #Fields
    fans = request.form.get('fans')
    category = request.form.get('category')
    description = request.form.get('description')
    id = request.form.get('id')
    name = request.form.get('name')
    website = request.form.get('website')

    loopCount = 0
    for x in fans,category,description,id,name,website:
        if x != None:
            if loopCount == 0:
                fields = fields + x
                loopCount = 1
            else:
                fields= fields + "," +x
    if loopCount == 0:
        fields = None


    #Post fields
    type = request.form.get('type')
    likes = request.form.get('likes')
    comments = request.form.get('comments')
    time = request.form.get('time')
    message = request.form.get('message')

    postfields = ",posts.fields("
    loopCount = 0
    graph_likes = 0
    graph_comments = 0
    for x in type,likes,comments,time,message:
        if x != None:
            if x == likes:
                graph_likes = 1;
            if x == comments:
                graph_comments = 1;
            if loopCount == 0:
                postfields = postfields + x
                loopCount = 1
            else:
                postfields= postfields + "," +x
    postfields = postfields + ")"
    if loopCount == 0:
        postfields = ",posts.fields()"

    if fields == None and postfields == None:
        url = 'http://seng3011laser.com/api/v2/PageData?company=' + company + '&startdate=' +startdate + '&enddate=' + enddate
    elif fields == None and postfields != None:
        url = 'http://seng3011laser.com/api/v2/PageData?company=' + company + '&startdate=' + startdate + '&enddate=' + enddate + "&fields=" + postfields
    elif postfields == None:
        url = 'http://seng3011laser.com/api/v2/PageData?company=' + company + '&startdate=' + startdate + '&enddate=' + enddate + fields
    else:
        url = 'http://seng3011laser.com/api/v2/PageData?company=' + company + '&startdate=' + startdate + '&enddate=' + enddate + fields + postfields
    # send request, get response
    print(url)
    response = requests.get(url)

    responseDict = response.json()

    if message != None and responseDict['Facebook Statistic Data'] != 'Error':

        for key,value in enumerate(responseDict['Facebook Statistic Data']['posts']):
            sentiment = client.Sentiment({'text': value['post_message'] })
            responseDict['Facebook Statistic Data']['posts'][key]['Message Polarity'] = sentiment['polarity']
            responseDict['Facebook Statistic Data']['posts'][key]['Message Subjectivity'] = sentiment['subjectivity']
    graph_data=""
    graphTitle=""
    if time != None and responseDict['Facebook Statistic Data'] != 'Error':
        #posts count, commets count, likes count
        timedict = {}
        likesdict = {}     
        commentsdict = {}
        for key, value in enumerate(responseDict['Facebook Statistic Data']['posts']):
            if (value['post_created_time'][:10]) not in timedict:
                timedict[(value['post_created_time'][:10])] = 1
                if (graph_likes): 
                    likesdict[(value['post_created_time'][:10])] = value['post_like_count']
                if (graph_comments):
                    commentsdict[(value['post_created_time'][:10])] = value['post_comment_count']
            else:
                timedict[(value['post_created_time'][:10])] = timedict[(value['post_created_time'][:10])] + 1
                if (graph_likes):
                    likesdict[(value['post_created_time'][:10])] = likesdict[(value['post_created_time'][:10])] + value['post_like_count']
                if (graph_comments):
                    commentsdict[(value['post_created_time'][:10])] = commentsdict[(value['post_created_time'][:10])] + value['post_comment_count']
                
                
        dateline = pygal.DateLine(x_label_rotation=25)
        dateline.x_labels = []
        #dateline.x_labels.append(date(int(startdate[:4]), int(startdate[5:7]), int(startdate[8:10])))
        dateline.x_labels.append(date(int(enddate[:4]), int(enddate[5:7]), int(enddate[8:10])))
        if (graph_likes):
            likescount = []
            count = 0;
            for key in likesdict:
                if count % 2:
                    dateline.x_labels.append(date(int(key[:4]), int(key[5:7]), int(key[8:10])))
                likescount.append((date(int(key[:4]), int(key[5:7]), int(key[8:10])),likesdict[key]))
                count+=1
        
        if (graph_comments):
            commentscount = []
            count = 0;
            for key in commentsdict:
                if count % 2:
                    dateline.x_labels.append(date(int(key[:4]), int(key[5:7]), int(key[8:10])))
                commentscount.append((date(int(key[:4]), int(key[5:7]), int(key[8:10])),commentsdict[key]))
                count+=1
            
        datecount = []
        count = 0;
        for key in timedict:
            if count % 2:
                dateline.x_labels.append(date(int(key[:4]), int(key[5:7]), int(key[8:10])))
            datecount.append((date(int(key[:4]), int(key[5:7]), int(key[8:10])),timedict[key]))
            count+=1
        if (graph_comments):
            dateline.add("Comments Count", commentscount)
        if (graph_likes):
            dateline.add("Likes Count", likescount)
        if (graph_comments==0 and graph_likes==0):
            dateline.add("Posts Count", datecount)
            graphTitle = 'Posts Count of ' + company + " from " +startdate[:4]+ "-" +startdate[5:7]+"-" + startdate[8:10] +" to " + enddate[:4]+"-" +enddate[5:7] +"-"+ enddate[8:10]
        else:
            graphTitle = 'Comments & Likes Count of ' + company + " from " +startdate[:4]+ "-" +startdate[5:7]+"-" + startdate[8:10] +" to " + enddate[:4]+"-" +enddate[5:7] +"-"+ enddate[8:10]
        graph_data = dateline.render_data_uri()

    return render_template("gui.html", company1 = responseDict,graph_data=graph_data,graphTitle=graphTitle)


if __name__ == '__main__':
    app.run()