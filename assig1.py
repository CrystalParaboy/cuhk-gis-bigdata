# Haversine formula, distance between two coordinates

from math import radians, degrees, sin, cos, asin, acos, sqrt

def great_circle(lon1, lat1, lon2, lat2):
  radius_of_earth = 6371
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
  return radius_of_earth * (acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)))


import requests
def getGeoCoord(address,key):
  base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
  url = base_url+'address='+address.replace(' ', '+')+'&key='+API_KEY
  response = requests.get(url,timeout=10)
  data = response.json()
  if data['status'] == 'OK':
    result = data['results'][0]
    location = result['geometry']['location']
    return location['lat'], location['lng']
  else:
    print("error: "+address)
    return 0

API_KEY = 'AIzaSyAz8tJ0SZb6ah0v376CwNM1BnBQnctWHB8'
address = 'Tsim Sha Tsui Station'

#2.1 Find the coordinate of Tsim Sha Tsui Station
TSTS_cor = getGeoCoord(address,API_KEY)
print("the coordinate of Tsim Sha Tsui Station:")
print(TSTS_cor)

#2.2 Find all coordinates of the addresses in Wellcome website
add = []
coor = []
with open('/content/wellcome stores.csv','r') as infile:
  for line in infile:
    res = getGeoCoord(line,API_KEY)
    if res != 0:
      coor.append(res)
      add.append(line)
  
print("address and coor of wellcome:")
for x in range(len(coor)):
  print(x, add[x], coor[x])



#2.3 Calculate the distance between Tsim Sha Tsui Station and each Wellcome store. Print those within 1km
distances = []
i=0
print("the list of those within 1km: ")
for co in coor:
  dis = great_circle(co[1], co[0], TSTS_cor[1], TSTS_cor[0])
  distances.append(dis)
  if dis <= 1:
    print(add[i],": ",coor[i]," dis = ", dis)
  i+=1
