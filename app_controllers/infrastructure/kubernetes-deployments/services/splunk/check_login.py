import sys, os
import splunklib.client as client

HOST = "splunk-charles-management.us-west1-a.securethebox.us"
PORT = 8089
USERNAME = "admin"
PASSWORD = "Changeme"

service = client.connect(
    scheme="http",
    version=7.3,
    host=HOST,
    port=80,
    username=USERNAME,
    password=PASSWORD)

for app in service.apps:
    print(app.name)