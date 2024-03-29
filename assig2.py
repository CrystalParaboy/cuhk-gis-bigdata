import requests
import folium

YOUR_KEY = 'AIzaSyBTNR-hSNnfH_yXc8ETDptjegAAePuM4s4'
BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={0}&location={1}&radius={2}&type={3}&keyword={4}'  
lat_ = 30.619779
lng_ = 114.257871

def jsonFormat(res):
  # return all the result in a dict with coordinate
  # {'a':[23.23,112.213], 'b':[31.552,127.831]}
  c=dict()# empty dict  as container
  for i in res['results']:
    c[i['name']] = [float(i['geometry']['location']['lat']),float(i['geometry']['location']['lng'])]
  return c


def nearBySearch(lat, lng, radius, placeType = '', keyword = ''):
  latlng = str(lat) + ',' + str(lng)
  url = BASE_URL.format(YOUR_KEY, latlng, radius, placeType, keyword)
  #print(url)
  response = requests.get(url,timeout=10)
  data = response.json()
  print(data)
  if data['status'] == 'OK':
    return jsonFormat(data)
  else:
    print("error: "+ url)
    return

radius_test = '2000' #500 meters
typecode_test = 'hosptial' # lets get some restaurants
hosptials = nearBySearch(lat_, lng_, radius_test, typecode_test)

folium.TileLayer(tiles = google_road_map, attr = 'Google Maps').add_to(map_plot4)

# popular basemap url
google_road_map = 'http://mt.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
google_satallite_map = 'http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}'
gaode = 'http://wprd03.is.autonavi.com/appmaptile?style=7&x={x}&y={y}&z={z}' 
tencent = 'http://rt1.map.gtimg.com/tile?z={z}&x={x}&y={-y}&styleid=1&version=117'

ManyMaps = folium.Map(location=[lat_,lng_], zoom_start=16)

# add them as the optional basemap 
folium.TileLayer(tiles=google_satallite_map, attr='Google Satellite', name= 'Google Satellite').add_to(ManyMaps)
folium.TileLayer(tiles=gaode, attr='高德地图',name = '高德地图').add_to(ManyMaps)
folium.LayerControl().add_to(ManyMaps)



for k in hosptials:
  folium.Marker(hosptials[k], tooltip=k).add_to(ManyMaps)

ManyMaps
