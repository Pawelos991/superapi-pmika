from locust import HttpUser, task
import imageio


class WebsiteUser(HttpUser):

    @task
    def prime(self):
        self.client.get(url='prime/13')

    @task
    def invert(self):
        in_file = open("testimg.jpg", "rb")
        data = in_file.read()
        self.client.post(url='picture/invert', files={'file': data})

    @task
    def getTime(self):
        self.client.get(url='get-time', headers={"username": "pmika", "password": "!QAZxsw2"})
