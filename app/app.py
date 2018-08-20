import requests
import datetime
import time
import scrollphat
import sys, signal
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_hours():
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7 # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
    mon = today - datetime.timedelta(idx-1)
    sun = today + datetime.timedelta(7-idx)

    pFrom = '{:%Y-%m-%d}'.format(mon)
    pTo = '{:%Y-%m-%d}'.format(sun)

    headers = {'Harvest-Account-ID': '348473', 'Authorization': 'Bearer 29707.pt.Ae8ToqIuwwTuNkWvq_ul7qFJJP0XAU8-K1yqHY6iUuW_GZLVznIC0RPA6Dvm59wtOKrbMfLNLqooSeLhyYYZrA'}
    params = {'from': pFrom, 'to': pTo}
    r = requests.get('https://api.harvestapp.com/api/v2/time_entries', headers=headers, params=params)
    body = r.json()

    total = 0.0
    for entry in body['time_entries']:
        total += entry['hours']


    return '{0:04.1f}'.format(total).replace('.', '')

scrollphat.set_brightness(200)
while True:
    hours = get_hours()
    print(hours)
    scrollphat.write_string(hours)
    time.sleep(50)

