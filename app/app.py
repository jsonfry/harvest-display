import datetime
import os
import requests
import scrollphat
import sys, signal
import time

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# from env
HARVEST_ACCOUNT_ID = os.getenv('HARVEST_ACCOUNT_ID')
HARVEST_PERSONAL_ACCESS_TOKEN = os.getenv('HARVEST_PERSONAL_ACCESS_TOKEN')
BRIGHTNESS=int(os.getenv('BRIGHTNESS'))

def get_hours():
    today = datetime.date.today()
    mon = today - datetime.timedelta(days=today.weekday())
    sun = mon + datetime.timedelta(days=6)

    pFrom = '{:%Y-%m-%d}'.format(mon)
    pTo = '{:%Y-%m-%d}'.format(sun)

    headers = {'Harvest-Account-ID': HARVEST_ACCOUNT_ID, 'Authorization': 'Bearer ' + HARVEST_PERSONAL_ACCESS_TOKEN}
    params = {'from': pFrom, 'to': pTo}
    r = requests.get('https://api.harvestapp.com/api/v2/time_entries', headers=headers, params=params)
    body = r.json()

    total = 0.0
    for entry in body['time_entries']:
        total += entry['hours']


    return '{0:04.1f}'.format(total).replace('.', '')

scrollphat.set_brightness(BRIGHTNESS)
while True:
    hours = get_hours()
    print(hours)
    scrollphat.write_string(hours)
    time.sleep(50)

