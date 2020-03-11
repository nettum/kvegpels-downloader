import requests
from clint.textui import progress
from os import path
from datetime import date, timedelta
from time import sleep


# But no one has seen or heard from him since last Wednesday
today = date.today()
delta = offset = (today.weekday() + 4) % 7 + 1
lastWednesday = today - timedelta(days=delta)

downloadPath = path.dirname(path.realpath(__file__)) + '/downloads/'
numFailedRequests = 0
weekDiffs = 0

while numFailedRequests < 10:
    dlDate = lastWednesday - timedelta(weeks=weekDiffs)
    filename = 'kvegpels_' + dlDate.strftime('%Y%m%d') + '.mp3'
    weekNumber = dlDate.strftime('%V')
    year = dlDate.strftime('%Y')
    dlUrl = f"http://dread.radionova.no/kringlast/kvegpels/{filename}"
    if path.exists(downloadPath + filename):
        print(f"Skip download of kvegpels week {weekNumber} {year}, {filename} already exists")
    else:
        print(f"Downloading kvegpels week {weekNumber} {year}: {dlUrl}")
        response = requests.get(dlUrl, stream=True)
        if response.status_code == 200:
            with open(downloadPath + filename, 'wb') as file:
                contentLength = int(response.headers.get('content-length'))
                for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(contentLength / 1024) + 1): 
                    if chunk:
                        file.write(chunk)
                        file.flush()               
        else:
            print(f"Could not download kvegpels week {weekNumber} {year}: {dlUrl}, server returned status {response.status_code}")
            numFailedRequests += 1
    
    weekDiffs += 1
    # Radionova is awesome \o/ Do not DDoS them.
    sleep(3)

