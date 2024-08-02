import math
import pickle
import re
import json


class GeoUnit:
    def __init__(self, geouri: str):
        self.geouri = geouri
        self.name = ""
        self.latitude = 0
        self.longitude = 0
        self.within = None
        self.within1 = None
        self.neighbours = []
        self.direction = dict()
        self.within = None
        self.name_postcode_unit = ""











# calculate the proximity directions

#def getAtan2(y, x):
    #return math.atan2(y, x)


#def computeBearing(endpoint, startpoint):
 #   x1 = endpoint['lat']
  #  y1 = endpoint['long']
  #  x2 = startpoint['lat']
  ##  y2 = startpoint['long']

  #  radians = getAtan2((y1 - y2), (x1 - x2))  # the result in Raduis and to convert  it to degree we do the next step
# Here angle in degree
  #  compassReading = radians * (180 / math.pi)
#
  #  coordNames = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
  #  coordIndex = round(compassReading / 45)
   # if (coordIndex < 0):
     #   coordIndex = coordIndex + 8
#
   # return coordNames[coordIndex]  # returns the coordinate value
#


# https://www.analytics-link.com/post/2018/08/21/calculating-the-compass-direction-between-two-points-in-python

def getAtan2(y, x):
    return math.atan2(y, x)


def compute_bearing(endpoint, startpoint):
    x1 = endpoint['lat']
    y1 = endpoint['long']
    x2 = startpoint['lat']
    y2 = startpoint['long']

    radians = getAtan2((y1 - y2), (x1 - x2))

    compassReading = radians * (180 / math.pi)

    if compassReading < 0:
        compassReading = compassReading + 360

    # https://www.ruralvt.com/ancientroads/bearingDistanceCalculations.php
    coordNames = ["N", "E", "S", "W", "N"]
    coordIndex = round(compassReading / 90)

    return coordNames[coordIndex] # returns the coordinate value

# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def compute_distance(endpoint, startpoint):
    # approximate radius of earth in km
    R = 6373.0
    x1 = math.radians(endpoint['lat'])
    y1 = math.radians(endpoint['long'])
    x2 = math.radians(startpoint['lat'])
    y2 = math.radians(startpoint['long'])

    dlon = y2 - y1
    dlat = x2 - x1
    a = (math.sin(dlat/2))**2 + math.cos(x1) * math.cos(x2) * (math.sin(dlon/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance



def compute_bearing_distance_all_coordinators(all_unit_coordinators: dict):
    all_nearest_by_directions = dict()
    list_unit_uris = list(all_unit_coordinators.keys())
   # to catch the current and next point
    for current_unit_uri in list_unit_uris:
        nearest_by_directions = dict() # to save the bearing result and check the distance
        # by tracking uri we can know the lat and long.
        current_unit_coordinator = all_unit_coordinators[current_unit_uri]
        for next_unit_uri in list_unit_uris:
            if next_unit_uri != current_unit_uri:
                next_unit_coordinator = all_unit_coordinators[next_unit_uri]
                # compute bearing and distance
                bearing = compute_bearing(next_unit_coordinator, current_unit_coordinator)
                distance = compute_distance(next_unit_coordinator, current_unit_coordinator)
                if bearing not in nearest_by_directions:
                    nearest_by_directions[bearing] = { 'uri': next_unit_uri, 'distance': distance}
                else:
                    current_nearest_unit = nearest_by_directions[bearing]
                    if distance < current_nearest_unit['distance']:
                        nearest_by_directions[bearing] = {'uri': next_unit_uri, 'distance': distance}

        all_nearest_by_directions[current_unit_uri] = nearest_by_directions

    return all_nearest_by_directions

#open the file of data and performe the function
def update_nearest_direction(geounit_pickle_path):
    with open(geounit_pickle_path,"rb") as infile:
        all_units = pickle.load(infile)



    all_unit_coordinators = dict()

    for current_uri, current_geounit in all_units.items():
        print(f"processing .............. {current_uri}")

        current_coordinator = {"lat": current_geounit.latitude, "long": current_geounit.longitude}
        all_unit_coordinators[current_uri] = current_coordinator

        # get results of computing nearest distance by direction
    all_nearest_by_directions = compute_bearing_distance_all_coordinators(all_unit_coordinators)
    # update nearest units by direction
    for current_uri, current_geounit in all_units.items():
        current_geounit.direction = all_nearest_by_directions[current_uri]

    with open(geounit_pickle_path, "wb") as outfile:
        pickle.dump(all_units, outfile, pickle.HIGHEST_PROTOCOL)





#open the file of data and performe the function
def update_nearest_direction_n(geounit_pickle_path):
    with open(geounit_pickle_path,"rb") as infile:
        all_units = pickle.load(infile)
    all_unit_coordinators = dict()
    with open("local_wales_district.pickle", "rb") as infile:
        all_districts = pickle.load(infile)


    for uri in all_districts.keys():


         for current_uri, current_geounit in all_units.items():
              print(f"processing .............. {current_uri}")

              current_coordinator = {"lat": current_geounit.latitude, "long": current_geounit.longitude}
              all_unit_coordinators[current_uri] = current_coordinator

        # get results of computing nearest distance by direction
         all_nearest_by_directions = compute_bearing_distance_all_coordinators(all_unit_coordinators)
    # update nearest units by direction
         for current_uri, current_geounit in all_units.items():
                 current_geounit.direction = all_nearest_by_directions[current_uri]

    with open(geounit_pickle_path, "wb") as outfile:
        pickle.dump(all_units, outfile, pickle.HIGHEST_PROTOCOL)





def convert_geounit_pickle2json(pickle_filepath):
    with open(pickle_filepath, 'rb') as infile:
        all_units = pickle.load(infile)

    list_geounits = []
    for uri, geounit in all_units.items():
        json_item = dict()
        json_item["uri"] = uri
        json_item["name"] = geounit.name
        json_item["lat"] = geounit.latitude
        json_item["long"] = geounit.longitude
        json_item["within"] = geounit.within
        json_item["within1"] = geounit.within1
        json_item["neighbours"] = geounit.neighbours
        json_item["direction"] = geounit.direction


        list_geounits.append(json_item)

    json_filepath = pickle_filepath.replace(".pickle", ".json")
    # write the json file
    with open(json_filepath, 'w', encoding='utf-8') as outfile:
        json.dump(list_geounits, outfile, ensure_ascii=False, indent=4)

# with open, we load the file into the python object.




def convert_json2pickle(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as infile:
        all_units = json.load(infile)

    list_geounits = dict()
    # list_geounits[uri] = geounit
    for unit in all_units:
        uri = unit['uri']
        geounit = GeoUnit(geouri=uri)
        geounit.name = unit['name']
        geounit.latitude = unit['lat']
        geounit.longitude = unit['long']
        geounit.within = unit['within']
        geounit.neighbours = unit['neighbours']
        geounit.direction = unit['direction']

        # save to dict
        list_geounits[uri] = geounit

    pickle_filepath = json_filepath.replace(".json", ".pickle")

    with open(pickle_filepath, 'wb') as outfile:
        pickle.dump(list_geounits, outfile, pickle.HIGHEST_PROTOCOL)

def convert_json2pickle_matched(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as infile:
        all_units = json.load(infile)

    list_geounits = dict()
    # list_geounits[uri] = geounit
    for unit in all_units:
        uri = unit['uri']
        geounit = GeoUnit(geouri=uri)
        geounit.name = unit['name']
        geounit.latitude = unit['lat']
        geounit.longitude = unit['long']
        geounit.within = unit['within']
        geounit.within = unit['within1']
        geounit.neighbours = unit['neighbours']
        geounit.direction = unit['direction']
        geounit.name_postcode_unit = unit['name_postcode_unit']

        # geounit.within = unit['within'] if 'within' in unit else ''


        # save to dict
        list_geounits[uri] = geounit

    pickle_filepath = json_filepath.replace(".json", ".pickle")

    with open(pickle_filepath, 'wb') as outfile:
        pickle.dump(list_geounits, outfile, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":



       #convert_geounit_pickle2json("local_wales_district.pickle")
      #convert_geounit_pickle2json("local_wales_wards.pickle")
      #convert_geounit_pickle2json("local_wales_parishes.pickle")
       #convert_geounit_pickle2json("local_wales_places_v2.pickle")
       #convert_geounit_pickle2json("local_wales_postalarea.pickle")
        #convert_geounit_pickle2json("local_wales_postal_district.pickle")
       #convert_geounit_pickle2json("local_wales_postal_sector.pickle")
        #convert_geounit_pickle2json("local_wales_postal_unit_s.pickle")
       # convert_geounit_pickle2json("local_wales_postal_unit_w.pickle")
        # convert_geounit_pickle2json("wales_uri2name_district.pickle")
          #convert_geounit_pickle2json("local_wales_postal_unit.pickle")
       # geounit_pickle_path = "local_wales_district.pickle"
       # update_nearest_direction(geounit_pickle_path)


     #geounit_pickle_path = "local_wales_wards.pickle"
     #update_nearest_direction(geounit_pickle_path)

       #geounit_pickle_path = "local_wales_parishes.pickle"
      # update_nearest_direction(geounit_pickle_path)

        #
        # geounit_pickle_path = "local_wales_places.pickle"
        # update_nearest_direction_n(geounit_pickle_path)
        #   geounit_pickle_path = "local_wales_places_v2.pickle"
        #   update_nearest_direction(geounit_pickle_path)
         # geounit_pickle_path = "LL_wales_postal_unit.json"
         # update_nearest_direction(geounit_pickle_path)


        #geounit_pickle_path = "local_wales_postal_unit_s.pickle"
        #update_nearest_direction(geounit_pickle_path)
         # #
         # geounit_pickle_path = "local_wales_postal_unit_in_SY.pickle"
         # update_nearest_direction(geounit_pickle_path)

        # convert_json2pickle("local_wales_places_v2.json")
           #convert_json2pickle_matched("matched_name_post_code.json")



         #convert_json2pickle("local_wales_two_places.json")
          convert_json2pickle("place_ward_postcode_unit.json")
           #geounit_pickle_path = "try_postal_unit_inside_sector.pickle"
           #update_nearest_direction(geounit_pickle_path)

        # convert_geounit_pickle2json("local_wales_places_first.pickle")
        # convert_geounit_pickle2json("local_wales_places_second.pickle")