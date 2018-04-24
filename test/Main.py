from unittest import TestCase
from __init__ import app  # Kinda weird idk
import csv


class BaseSettings(TestCase):
    def setUp(self):
        self.message = ""

        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        print("Complete: " + self.message)


class Registration(BaseSettings):
    def test_test(self):
        self.message = 'test_test'
        self.assertEqual(True, True, "True is true")

    def test_url_inputs(self):
        self.message = 'test_url_inputs'
        with open('testData/url.csv') as csv_urls:

            reader = csv.DictReader(csv_urls)
            test_case = 1

            for row in reader:
                result = self.app.get(row['URL'])
                self.assertEqual(int(row['StatusCode']), result.status_code, 'Test case ' + str(test_case) +
                                 ' failed with URL: ' + row['URL'] + '\n Data: ' + str(result.data))
                print('Test Case ' + str(test_case) + ' Successful')
                test_case += 1

    