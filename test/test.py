from locust import HttpLocust, TaskSet, task

class UserBehaviour(TaskSet):
    @task(1)
    def index(self):
        self.client.get("/api/woolworths?statistics=posts%7Bid%2C%20message%7D&access_token=EAACEdEose0cBAEikTeJjYD6IpjxSea4rQ5c3z3bbkJNrr6r7vMBy3LIEGZCCPRjPhiuyJ3T3XgZAVUtW5IMvrjLPuZApjo1dQR3meZB8pEY6PMZAA7QiZBEnf4MG9gpoUcsXNzwKyhQCaiKPFxfPnzWG0xc4dXB2P0EqAB9ajELTthNlviv8eYZB9zFIt3cGu5ZAvFWbewZBh8gZDZD")

class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    min_wait = 5000
    max_wait = 9000