from locust import HttpUser, between, task


class DefaultUser(HttpUser):

    # wait between requests from one user for between 1 and 5 seconds.
    wait_time = between(0.1, 0.5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def check_health(self):
        with self.client.get("/expenses", catch_response=True) as response:
            if response.text != "OK":
                response.failure("Wrong response.")
