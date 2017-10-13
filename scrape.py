import requests
from time import sleep
from firebase import firebase

SEGMENTS = [
    {
        'name': 'Upham Street Westbound',
        'description': 'From E. Woodcrest Drive to Ardsmoor Road',
        'from': 'x:-71.0400652885437 y:42.46070020618722',
        'to': 'x:-71.04659914970398 y:42.459283387705106',
    },
    {
        'name': 'Upham Street Eastbound',
        'description': 'Lincoln to E. Woodcrest',
        'from': 'x:-71.053017 y:42.458298',
        'to': 'x:-71.040024 y:42.460704',
    },
    {
        'name': 'Howard Street Westbound',
        'description': 'Saugus to Hesseltine Ave',
        'from': 'x:-71.04748964309692 y:42.46970693925081',
        'to': 'x:-71.05745673179626 y:42.46688159218133',
    },
    {
        'name': 'Howard Street Eastbound',
        'description': 'From Hesseltine Ave to Saugus',
        'from': 'x:-71.05745673179626 y:42.46688159218133',
        'to': 'x:-71.04748964309692 y:42.46970693925081',
    },
    {
        'name': 'Franklin Street Westbound',
        'description': 'From Garden St. to Ferdinan',
        'from': 'x:-71.07273459434509 y:42.469192529812155',
        'to': 'x:-71.07844233512878 y:42.47060912405725',
    },
    {
        'name': 'Franklin Street Eastbound',
        'description': 'From Ferdinand to Garden St.',
        'from': 'x:-71.07844233512878 y:42.47060912405725',
        'to': 'x:-71.07273459434509 y:42.469192529812155',
    },

]


db = firebase.database()


def get_speed(origin='', destination=''):

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept-language': 'en-US,en;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'x-requested-with': 'XMLHttpRequest',
        'referer':'https://www.waze.com/livemap',
    }

    resp = requests.get('https://www.waze.com/livemap')

    resp = requests.get('https://www.waze.com/login/get', headers=headers)

    cookies = resp.cookies

    params = {
        'from': origin,
        'to': destination,
        'at': 0,
        'returnJSON': True,
        'returnGeometries': False,
        'returnInstructions': False,
        'options': 'AVOID_TRAILS:t,ALLOW_UTURNS:t',
    }

    url = 'https://www.waze.com/RoutingManager/routingRequest'

    resp = requests.get(url, headers=headers, cookies=cookies, params=params)

    data = resp.json()

    totalTime = data['response']['totalRouteTime']

    totalDistance = 0

    for i in data['response']['results']:
        totalDistance = totalDistance + i['length']

    miles = totalDistance / 1609.34

    hours = float(totalTime) / 60 / 60

    speed = miles / hours

    return speed

for segment in SEGMENTS:
    speed = get_speed(segment['to'], segment['from'])

    print "%s: %s mph" % (segment['name'], speed)

    db.child('speeds').child(segment['name']).push({
        'name': segment['name'],
        'description': segment['description'],
        'speed': speed,
    })

    sleep(1)


