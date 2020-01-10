import requests, json 
maps_api_key = 'AIzaSyC6ZIX6HQapsI2qQK6g1osuDYXBe8ZDfYs'

def storeType(query):
    #base url for google maps api requests
    base_map_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    response = requests.get(base_map_url + 'query=' + query +'&key=' + maps_api_key)
    places = response.json()['results']
    storeTypes = map(getTypes,places)
    print(list(storeTypes))
    
def getTypes(placeObject):
    return placeObject['types']
