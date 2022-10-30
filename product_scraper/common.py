import random
import time

def short_sleep():

    time.sleep(random.randrange(10, 20))

def long_sleep():

    time.sleep(random.randrange(20, 50))

def log_action(log_json):

    print(log_json)