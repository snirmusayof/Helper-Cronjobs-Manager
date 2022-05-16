import request
import os
import stat
import json
import base64
import socket
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLUSER_NAME = (os.environ.get('CLUSTER_NAME'))
BASE_DOMAIN = (os.environ.get('BASE_DOMAIN'))
USER = (os.environ.get('USER'))
PASSWORD = (os.environ.get('PASSWORD'))

SAVE_TESTS_PATH = '/var/CloudletOtherService'
SAVE_CRONJOBS_PATH = '/etc/cron.d'

def save_files(files, path_to_save):
    for filename in files:
        with open(f"{path_to_save}/{filename}", 'w') as file:
            file.write(base64.base64decode(files[filename].encode()).decode())

def premission_tests(SAVE_TESTS_PATH):
    for file in os.listdir(f"{SAVE_TESTS_PATH}"):
        os.chmod(f"{SAVE_TESTS_PATH}/{file}", stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP)

def fetch_tests():
    response = requests.get(f"https://cronjobs-controller.apps.{CLUSER_NAME}.{BASE_DOMAIN}/tests", auth=(USER,PASSWORD), verify=False)
    tests = response.json()
    save_files(tests, SAVE_TESTS_PATH)

def fetch_cronjobs():
    response = requests.get(f"https://cronjobs-controller.apps.{CLUSER_NAME}.{BASE_DOMAIN}/cronjobs", auth=(USER,PASSWORD), verify=False)
    cronjobs = response.json()
    save_files(tests, SAVE_CRONJOBS_PATH)

def check_status():
    try:
        fetch_tests()
        premission_tests(SAVE_TESTS_PATH)
        fetch_cronjobs()
    except Exception as err:
        return str(err)
    return "Download tests and cronjobs successfully\n"

def main():
    while True:
    print(check_status())
    time.sleep(180)

if __name__ == "__main__":
    main()
