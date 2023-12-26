import os
import random
from locust import HttpUser, task

persistent_ids = []
cwd = os.getcwd()
persistent_id_file = os.path.join(cwd, 'persistent_id.txt')
with open(persistent_id_file, 'r') as f:
    persistent_ids = [line.strip() for line in f]


class ItunesDataUser(HttpUser):
    @task(1)
    def get_ping(self):
        self.client.get("/ping")

    @task(5)
    def get_persistent_id(self):
        id = random.choice(persistent_ids)

        self.client.get(f"/itunes_data/{id}", name="/itunes_data/<id>")

    @task(2)
    def get_all_tracks(self):
        self.client.get("/itunes_data/")
