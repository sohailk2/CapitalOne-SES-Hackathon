import requests, json 
maps_api_key = 'AIzaSyC6ZIX6HQapsI2qQK6g1osuDYXBe8ZDfYs'

# https://maps.googleapis.com/maps/api/place/textsearch/json?
# location=-33.8670522,151.1957362
# &query=gas
# &key=AIzaSyC6ZIX6HQapsI2qQK6g1osuDYXBe8ZDfYs

def getStoreType(location, query):
    #base url for google maps api requests
    base_map_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    response = requests.get(base_map_url + 'latitude=' + location + '&query=' + query +'&key=' + maps_api_key)
    places = response.json()['results']

    if (places):
        storeTypes = list(map(getTypes,places))
        return storeTypes[0]
    else:
        return None

    
def getTypes(placeObject):
    return placeObject['types']


# before after
# confused person on what to use
# 