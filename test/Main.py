from unittest import TestCase
from __init__ import app  # Kinda weird idk
import csv
import jsonpickle
import requests
import re
#
# NOTE: endpoint for tests now configurable with the value in endpoint.json which should be either seng3011laser.com,
# localhost:5000, or blank for internal test
#

class BaseSettings(TestCase):
    def setUp(self):
        self.message = ""

        self.app = app.test_client()
        self.app.testing = True

        with open('endpoint.json') as endpoint_data:
            endpoint = jsonpickle.decode(endpoint_data.read())['endpoint']
         #   if endpoint == 'seng3011laser.com' or endpoint == 'localhost:5000':
            self.endpoint = 'http://' + endpoint
            self.getResponse = self.urlGet
         #   else:
           #     self.endpoint = ''
           #     self.getResponse = self.internalGet


    def tearDown(self):
        print("Complete: " + self.message)


class Registration(BaseSettings):
    def test_test(self):
        self.message = 'test_test'
        self.assertEqual(True, True, "True is true")

    def test_url_inputs(self):
        self.message = 'test_url_inputs'
        with open('testData/crushingbeasts.csv') as csv_urls:

            reader = csv.DictReader(csv_urls)
            test_case_no = 1

            for row in reader:
                result, code = self.getResponse(row['URL'])
                self.assertEqual(int(row['StatusCode']), code, 'Test case ' + str(test_case_no) +
                                 ' failed with URL: ' + row['URL'])
                print('Test Case ' + str(test_case_no) + ' Successful')
                test_case_no += 1

    def     test_response_fields(self):
        self.message = 'test_response_fields'
        with open('testData/response_fields.json') as json_file:

            test_cases = jsonpickle.decode(json_file.read())['test_cases']
            test_case_no = 1

            for test_case in test_cases:
                #Use the URL builder for the correct API
               # result, code = self.getAPIResponse(test_case)
               # result, code = self.getMooseResponse(test_case)
             #   result, code = self.getUnassignedResponse(test_case)
                result, code = self.getCrushingBeastsResponse(test_case)
                self.assertEqual(code, 200)
                result_dict = jsonpickle.decode(result)
                result_fb_info = result_dict['Facebook Statistic Data']
                #result_dict['data'] for unassigned and moose, Facebook Statistic for laser and crushing beasts
              #  result_fb_info = result_dict['data']

                #  Check that if we are expecting a field (according to test_case) that the field is actually in the result
                for key in test_case['page_fields_output']:

                    print(key)
                    for key2 in result_fb_info:
                        key3 = re.sub('[^a-zA-Z ]+', '', key)
                        key3 = key3.lower()
                        key4 = re.sub('[^a-zA-Z ]+', '', key2)
                        key4 = key4.lower()
                        if key3 == key4:
                           self.assertEqual(key in test_case['page_fields_output'], key2 in result_fb_info)

              #  self.assertEqual("PageId" in test_case['page_fields_output'], "PageId" in result_fb_info)
                #  self.assertEqual("PageName" in test_case['page_fields_output'], "PageName" in result_fb_info)
              #  self.assertEqual("Description" in test_case['page_fields_output'], "Description" in result_fb_info)
              #  self.assertEqual("Category" in test_case['page_fields_output'], "Category" in result_fb_info)
              #  self.assertEqual("FanCount" in test_case['page_fields_output'], "FanCount" in result_fb_info)
              #  self.assertEqual("Website" in test_case['page_fields_output'], "Website" in result_fb_info)
                print("done with page")
                if('posts' in result_fb_info):
                    self.assertEqual(len(test_case['posts_fields_output']) > 0, "post_id" in result_fb_info['posts'][0])
                    self.assertEqual("post_type" in test_case['posts_fields_output'], "post_type" in result_fb_info['posts'][0])
                    self.assertEqual("post_message" in test_case['posts_fields_output'], "post_message" in result_fb_info['posts'][0])

                    if "post_like_count" not in test_case['posts_fields_output']:
                        self.assertEqual("post_like_count" in test_case['posts_fields_output'],
                                         "post_like_comment" in result_fb_info['posts'][0])
                    else:
                        self.assertEqual("post_like_count" in test_case['posts_fields_output'],
                                         "post_like_count" in result_fb_info['posts'][0])
                    self.assertEqual("post_comment_count" in test_case['posts_fields_output'], "post_comment_count" in result_fb_info['posts'][0])
                    self.assertEqual("post_created_time" in test_case['posts_fields_output'], "post_created_time" in result_fb_info['posts'][0])
                else:
                    self.assertTrue(len(test_case['posts_fields_output']) == 0)


                print('Test Case ' + str(test_case_no) + ' Successful')
                test_case_no += 1

    def getAPIResponse(self, test_case):
        post_fields = test_case['post_fields_input']
        page_fields = test_case['page_fields_input']

        if len(page_fields) == 0 and len(post_fields) == 0:
            return self.getResponse('/api/v2/PageData?company=woolworths&startdate=2015-10-01T08:45:10.295Z&enddate=2015-11-01T19:37:12.193Z')
        elif len(post_fields) == 0:
            fields_string = ','.join(page_fields)
        elif len(page_fields) == 0:
            fields_string = 'posts.fields(' + ','.join(post_fields) + ')'
        else:
            fields_string = ','.join(page_fields) + ',posts.fields(' + ','.join(post_fields) + ')'

        response = self.getResponse('/api/v2/PageData?company=woolworths&startdate=2015-10-01T08:45:10.295Z&enddate=2015-11-01T19:37:12.193Z&fields=' + fields_string)

        return response


    #Build a url for moose
    def getMooseResponse(self, test_case):
        post_fields = test_case['post_fields_input']
        page_fields = test_case['page_fields_input']
      # "/v3/company?id=woolworths&start_date=2015-10-01T08:45:10.295Z&end_date=2015-11-01T19:37:12.193Z&stats=website,description"
        if len(page_fields) == 0 and len(post_fields) == 0:
            return self.getResponse('/v3/company?id=woolworths&start_date=2015-10-01T08:45:10.295Z&end_date=2015-11-01T19:37:12.193Z')

        fields_string = ','.join(page_fields)
        if len(post_fields) != 0:
            fields_string += ','
            fields_string += ','.join(post_fields)


        response = self.getResponse('/v3/company?id=woolworths&start_date=2015-10-01T08:45:10.295Z&end_date=2015-11-01T19:37:12.193Z&stats=' + fields_string)
        return response

    def getUnassignedResponse(self, test_case):
        post_fields = test_case['post_fields_input']
        page_fields = test_case['page_fields_input']

        if len(page_fields) == 0 and len(post_fields) == 0:
            return self.getResponse('/api/woolworths?&start_date=2015-10-01T08:45:10.295Z&end_date=2015-11-01T19:37:12.193Z&access_token=EAACEdEose0cBAETkyJI5hwZAOTYWht37yZAcZA6797wYVgZCjQZBSpfKnZCJGchxLp4inElTCoCla2LWurrT82M9prjNM14btC89YnEwznC93HnyaTMo05TcKafdwOsZBgHI7o6TMVoVTH6WcDDc2zEtDwatTWwG1DzozmfB0vZCZAqd8r9CbejLN7fZCro51844NnFIc78mMZAgQZDZD')

        else:
            fields_string = ','.join(page_fields)
        if len(post_fields) != 0:
            fields_string += ','
            fields_string += ','.join(post_fields)

        response = self.getResponse('/api/woolworths?statistics=' + fields_string + "&start_date=2015-10-01T08:45:10.295Z&end_date=2015-11-01T19:37:12.193Z" + '&access_token=EAACEdEose0cBAETkyJI5hwZAOTYWht37yZAcZA6797wYVgZCjQZBSpfKnZCJGchxLp4inElTCoCla2LWurrT82M9prjNM14btC89YnEwznC93HnyaTMo05TcKafdwOsZBgHI7o6TMVoVTH6WcDDc2zEtDwatTWwG1DzozmfB0vZCZAqd8r9CbejLN7fZCro51844NnFIc78mMZAgQZDZD')
        print(fields_string)
        return response

    def getCrushingBeastsResponse(self, test_case):
        post_fields = test_case['post_fields_input']
        page_fields = test_case['page_fields_input']

        if len(page_fields) == 0 and len(post_fields) == 0:
            return self.getResponse('/api/v1/fbstats?startdate=2015-10-1T0:0:0&enddate=2015-11-1T0:0:0&instid=wow&stats=id')
        else:
            fields_string = ','.join(page_fields)
        if len(post_fields) != 0:
            fields_string += ',posts{'
            fields_string += ','.join(post_fields)
            fields_string += '}'

        response = self.getResponse('/api/v1/fbstats?startdate=2015-10-1T0:0:0&enddate=2015-11-1T0:0:0&instid=wow&stats=' + fields_string)

        return response



    def urlGet(self, url):
        response = requests.get(self.endpoint + url)
        return response.text, response.status_code

    def internalGet(self, url):
        response = self.app.get(self.endpoint + url)
        return response.data.decode('utf-8'), response.status_code
