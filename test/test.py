from locust import HttpLocust, TaskSet, task

class UserBehaviour(TaskSet):
    @task(1)
    def index(self):
        self.client.get("/api/v2/PageData?company=woolworths&startdate=2015-10-01T08:45:10.295Z&enddate=2015-11-01T19:37:12.193Z&fields=description,post.fields(post_message)")

class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    min_wait = 5000
    max_wait = 9000