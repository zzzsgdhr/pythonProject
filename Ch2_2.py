import json, requests

API_KEY = 'your API KEY here'


def getGeo(add):
  add = str(add).replace(' ', '+')
  quiry = \
    'https://maps.googleapis.com/maps/api/geocode/' \
    'json?address={}&key={}' \
      .format(
      add,
      API_KEY
    )
  response = requests.get(quiry)
  j = json.loads(response.text)
  return j.get('results')[0].get('geometry').get('viewport').get('southwest').values()


def getTimezone(val1, val2):
  quiry = \
    'https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp=1412649030&key={}'. \
      format(val1,
             val2,
             API_KEY)

  response = requests.get(quiry)
  j = json.loads(response.text)
  return j.get('timeZoneName'), j.get('timeZoneId')


if __name__ == '__main__':
  print(getTimezone(34.68, 113.65))
  address = input('Please input address:')
  q = list(getGeo(address))

  print(getTimezone(q[0], q[1]))
