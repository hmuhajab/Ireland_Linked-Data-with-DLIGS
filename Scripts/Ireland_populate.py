from owlready2 import *
#import dill as pickle
#from geo_unit import GeoUnit
import pickle
import json
from rdflib import BNode
from urllib.parse import unquote




def load_ontology():
    onto = get_ontology('ontology/Abstract_Updated.rdf').load()
    base_iri = onto.base_iri
    print(base_iri)

    proximity_directional = onto.proximity_directional


    with onto:
        class nearest_N(proximity_directional):
            pass

        class nearest_S(proximity_directional):
            pass

        class nearest_W(proximity_directional):
            pass

        class nearest_E(proximity_directional):
            pass


    return onto






def get_Ireland_Counties_information(onto):
    # Verify if Counties is a defined class in the ontology
    if not hasattr(onto, 'Counties'):
        print("Counties class not found in the ontology.")
        return None
    else:
        print("Found Counties class.")
    Counties = onto.Counties

    # Additional debug print to check the Counties class
    print("Counties class: ", Counties)

    counties = dict()

    with open('dataset_with_id/updated_counties.json', "r") as read_file:
        data = json.load(read_file)

    for item in data:
        try:
            print(f"Processing item: {item}")
            county = Counties(name=item["name"])
            if "within" in item:
                county.within = item["within"]
            if "direction" in item:
                county.direction = item["direction"]
            if "lat" in item and "long" in item:
                county.lat = item["lat"]
                county.long = item["long"]
            if "CO_ID" in item:  # Check if CO_ID is in the item and add it
                county.CO_ID = item["CO_ID"]
            counties[item["name"]] = county
        except Exception as e:
            print(f"Error processing item {item}: {e}")

    return counties



def populate_Ireland_counties(onto):
    Counties = onto.Counties
    counties = get_Ireland_Counties_information(onto)

    Administrative_hierarchy_of_Ireland1 = onto.Administrative_hierarchy_of_Ireland1
    Administrative_hierarchy_of_Ireland2 = onto.Administrative_hierarchy_of_Ireland2
    Administrative_hierarchy_of_Ireland3 = onto.Administrative_hierarchy_of_Ireland3
    Administrative_hierarchy_of_Ireland4 = onto.Administrative_hierarchy_of_Ireland4

    part_of = onto.part_of
    level_in_hierarchy = onto.level_in_hierarchy

    OSI_id = onto.OSI_id


    # Define the latitude and longitude properties
    lat = onto.lat
    long = onto.long

    ehInside = onto.ehInside
    print(ehInside)


    with onto:
        for name, county in counties.items():
            current = Counties(name, part_of=[Administrative_hierarchy_of_Ireland1, Administrative_hierarchy_of_Ireland2,
                                              Administrative_hierarchy_of_Ireland3,  Administrative_hierarchy_of_Ireland4],
                               level_in_hierarchy=1)
            if county.within:
                parent_name = county.within
                parent_instance = onto[parent_name]
                print(f"parent_instance for {parent_name}: {parent_instance}")
                if parent_instance is not None:
                    current.ehInside.append(parent_instance)

            latitude_value = county.lat
            longitude_value = county.long

            # Print latitude and longitude values for debugging
            # print(f"Latitude for {uri}: {latitude_value}")
            # print(f"Longitude for {uri}: {longitude_value}")

            # Set the latitude and longitude properties to the district instance
            if latitude_value is not None:
                current.lat = latitude_value  # Assign directly, no append
            if longitude_value is not None:
                current.long = longitude_value  # Assign directly, no append

            id = county.CO_ID
            if id is not None:
                current.OSI_id = id


            for bearing, values in county.direction.items():
                # note that: values is a dictionary: {'uri': uri, 'distance': distance}
                neighbour_name = values['name']
                neighbour = onto[neighbour_name]
                if bearing == "N":
                    current.nearest_N.append(neighbour)
                if bearing == "S":
                    current.nearest_S.append(neighbour)
                if bearing == "E":
                    current.nearest_E.append(neighbour)
                if bearing == "W":
                    current.nearest_W.append(neighbour)






# Barony


def get_Ireland_Baronies_information(onto):
    # Verify if Baronies is a defined class in the ontology
    if not hasattr(onto, 'Barony'):
        print("Barony class not found in the ontology.")
        return None
    else:
        print("Found Barony class.")
    Barony = onto.Barony

    # Additional debug print to check the Barony class
    print("Barony class: ", Barony)

    baronies = dict()

    with open('dataset_id_cleaned/updated_baronies_cleaned.json', "r") as read_file:
        data = json.load(read_file)

    for item in data:
        try:
            print(f"Processing item: {item}")
            barony = Barony(name=item["name"])
            if "within" in item:
                barony.within = item["within"]
            if "direction" in item:
                barony.direction = item["direction"]
            if "lat" in item and "long" in item:
                barony.lat = item["lat"]
                barony.long = item["long"]
            if "LOGAINM_RE" in item:  # Check if CO_ID is in the item and map it to OSI_id
                barony.OSI_id = item["LOGAINM_RE"]

            baronies[item["name"]] = barony
        except Exception as e:
            print(f"Error processing item {item}: {e}")

    return baronies


def populate_Ireland_baronies(onto):
    # Use the Barony class from the ontology
    Barony = onto.Barony
    Administrative_hierarchy_of_Ireland1 = onto.Administrative_hierarchy_of_Ireland1
    baronies = get_Ireland_Baronies_information(onto)

    with onto:
        for name, barony in baronies.items():
            current = Barony(name,
                               part_of=[Administrative_hierarchy_of_Ireland1],
                               level_in_hierarchy=2)
            if barony.within:
                parent_name = barony.within
                parent_instance = onto[parent_name]
                print(f"parent_instance for {parent_name}: {parent_instance}")
                if parent_instance is not None:
                    current.ehInside.append(parent_instance)

            latitude_value = barony.lat
            longitude_value = barony.long

            # Print latitude and longitude values for debugging
            # print(f"Latitude for {uri}: {latitude_value}")
            # print(f"Longitude for {uri}: {longitude_value}")

            # Set the latitude and longitude properties to the district instance
            if latitude_value is not None:
                current.lat = latitude_value  # Assign directly, no append
            if longitude_value is not None:
                current.long = longitude_value  # Assign directly, no append

            id = barony.OSI_id
            if id is not None:
                current.OSI_id = id

            for bearing, values in barony.direction.items():
                neighbour_name = values['name']
                neighbour = onto[neighbour_name]
                if neighbour is not None:  # Add this check
                    if bearing == "N":
                        current.nearest_N.append(neighbour)
                    if bearing == "S":
                        current.nearest_S.append(neighbour)
                    if bearing == "E":
                        current.nearest_E.append(neighbour)
                    if bearing == "W":
                        current.nearest_W.append(neighbour)


# Civil Parish



def get_Ireland_Civilparish_information(onto):
    cparish = dict()
    Civil_Parish = onto.Civil_Parish

    with open('dataset_id_cleaned/updated_CivilParish_cleaned.json', "r") as read_file:
        data = json.load(read_file)

    for item in data:
        cp = Civil_Parish(item["name"] +"_parish")
        if "within" in item:
            cp.within = item["within"]
        if "direction" in item:
            cp.direction = item["direction"]

        if "lat" in item and "long" in item:
            cp.lat = item["lat"]
            cp.long = item["long"]

        if "LOGAINM_RE" in item:  # Check if CO_ID is in the item and map it to OSI_id
            cp.OSI_id = item["LOGAINM_RE"]
        cparish[item["name"]] = cp

    return cparish

def populate_Ireland_Civil_Parish(onto):
    cparish = get_Ireland_Civilparish_information(onto)

    Administrative_hierarchy_of_Ireland1 = onto.Administrative_hierarchy_of_Ireland1
    Civil_Parish = onto.Civil_Parish
    part_of = onto.part_of
    level_in_hierarchy = onto.level_in_hierarchy
    ehInside = onto.ehInside
    lat = onto.lat
    long = onto.long

    with onto:
        for name, cp in cparish.items():
            current = Civil_Parish(name +"_parish", part_of=[Administrative_hierarchy_of_Ireland1], level_in_hierarchy=3)
            if cp.within:
                parent_name = cp.within
                parent_instance = onto[parent_name]
                if parent_instance is not None:
                   current.ehInside.append(parent_instance)

            latitude_value = cp.lat
            longitude_value = cp.long

                # Print latitude and longitude values for debugging
                # print(f"Latitude for {uri}: {latitude_value}")
                # print(f"Longitude for {uri}: {longitude_value}")

                # Set the latitude and longitude properties to the district instance
            if latitude_value is not None:
                current.lat = latitude_value  # Assign directly, no append
            if longitude_value is not None:
                current.long = longitude_value  # Assign directly, no append
            id = cp.OSI_id
            if id is not None:
                 current.OSI_id = id



            for bearing, values in cp.direction.items():

                neighbour_name = values['name'] +"_parish"
                neighbour = onto[neighbour_name]
                if neighbour is not None:
                    if bearing == "N":
                        current.nearest_N.append(neighbour)
                    if bearing == "S":
                        current.nearest_S.append(neighbour)
                    if bearing == "E":
                        current.nearest_E.append(neighbour)
                    if bearing == "W":
                        current.nearest_W.append(neighbour)


# district

def get_Ireland_district_information(onto):
    districts = dict()

    Municipal_Districts = onto.Municipal_Districts

    with open('dataset_id_cleaned/updated_district_cleaned.json', "r") as read_file:
        data = json.load(read_file)

    for item in data:
        district = Municipal_Districts(item["name"] + "_district")
        if "within" in item:
            district.within = item["within"]
        if "direction" in item:
            district.direction = item["direction"]

        if "lat" in item and "long" in item:
            district.lat = item["lat"]
            district.long = item["long"]
        if "MD_ID" in item:  # Check if CO_ID is in the item and map it to OSI_id
            district.OSI_id = item["MD_ID"]
        districts[item["name"]] = district

    return districts
def populate_Ireland_district(onto):
    districts = get_Ireland_district_information(onto)

    Administrative_hierarchy_of_Ireland2 = onto.Administrative_hierarchy_of_Ireland2
    Municipal_Districts = onto.Municipal_Districts
    part_of = onto.part_of
    level_in_hierarchy = onto.level_in_hierarchy
    ehInside = onto.ehInside
    lat = onto.lat
    long = onto.long

    with onto:
        for name, district in districts.items():
            current = Municipal_Districts(name + "_district", part_of=[Administrative_hierarchy_of_Ireland2], level_in_hierarchy=2)

            #if district and hasattr(district, 'within'):
            if district.within:
                parent_name = district.within
                parent_instance = onto[parent_name]
                if parent_instance is not None:
                    current.ehInside.append(parent_instance)

            latitude_value = district.lat
            longitude_value = district.long

            # Print latitude and longitude values for debugging
            # print(f"Latitude for {uri}: {latitude_value}")
            # print(f"Longitude for {uri}: {longitude_value}")

            # Set the latitude and longitude properties to the district instance
            if latitude_value is not None:
                current.lat = latitude_value  # Assign directly, no append
            if longitude_value is not None:
                current.long = longitude_value  # Assign directly, no append

            id = district.OSI_id
            if id is not None:
                current.OSI_id = id

            for bearing, values in district.direction.items():

                neighbour_name = values['name'] + "_district"
                neighbour = onto[neighbour_name]
                if neighbour is not None:
                    if bearing == "N":
                        current.nearest_N.append(neighbour)
                    if bearing == "S":
                        current.nearest_S.append(neighbour)
                    if bearing == "E":
                        current.nearest_E.append(neighbour)
                    if bearing == "W":
                        current.nearest_W.append(neighbour)




# Townland



def get_Ireland_townland_information(onto):
    townlands = dict()
    Townland = onto.Townland

    with open('dataset_id_cleaned/updated_townland_2_cleaned.json', "r") as read_file:
        data = json.load(read_file)

    for item in data:
        townland = Townland(item["name"] + "_townland")
        if "within" in item:
            townland.within = item["within"]
        if "within1" in item:
            townland.within1 = item["within1"]
        if "direction" in item:
            townland.direction = item["direction"]
        if "lat" in item and "long" in item:
            townland.lat = item["lat"]
            townland.long = item["long"]
        if "LOGAINM_RE" in item:  # Check if CO_ID is in the item and map it to OSI_id
            townland.OSI_id = item["LOGAINM_RE"]

        townlands[item["name"]] = townland

    return townlands

def populate_Ireland_townland(onto):
    townlands = get_Ireland_townland_information(onto)

    Administrative_hierarchy_of_Ireland1 = onto.Administrative_hierarchy_of_Ireland1
    Administrative_hierarchy_of_Ireland4 = onto.Administrative_hierarchy_of_Ireland4
    Townland = onto.Townland
    part_of = onto.part_of
    level_in_hierarchy = onto.level_in_hierarchy
    ehInside = onto.ehInside
    lat = onto.lat
    long = onto.long

    with onto:
        for name, townland in townlands.items():
            current = Townland(name + "_townland", part_of=[Administrative_hierarchy_of_Ireland1, Administrative_hierarchy_of_Ireland4],  level_in_hierarchy=4)
            if townland.within:
                parent_name = townland.within
                parent_instance = onto[parent_name]
                if parent_instance is not None:
                    current.ehInside.append(parent_instance)
            if townland.within1:
                parent_name = townland.within1
                parent_instance = onto[parent_name]
                if parent_instance is not None:
                     current.ehInside.append(parent_instance)

            latitude_value = townland.lat
            longitude_value = townland.long

            # Print latitude and longitude values for debugging
            # print(f"Latitude for {uri}: {latitude_value}")
            # print(f"Longitude for {uri}: {longitude_value}")

            # Set the latitude and longitude properties to the district instance
            if latitude_value is not None:
                current.lat = latitude_value  # Assign directly, no append
            if longitude_value is not None:
                current.long = longitude_value  # Assign directly, no append

            id = townland.OSI_id
            if id is not None:
                current.OSI_id = id

            for bearing, values in townland.direction.items():
                # note that: values is a dictionary: {'uri': uri, 'distance': distance}
                neighbour_name = values['name'] + "_townland"
                neighbour = onto[neighbour_name]
                if bearing == "N":
                    current.nearest_N.append(neighbour)
                if bearing == "S":
                    current.nearest_S.append(neighbour)
                if bearing == "E":
                    current.nearest_E.append(neighbour)
                if bearing == "W":
                    current.nearest_W.append(neighbour)


# province


def get_Ireland_province_information(onto):
    ps = dict()
    Provinces = onto.Provinces

    with open('dataset_with_id/p.json', "r") as read_file:
        data = json.load(read_file)

    for item in data:
        p = Provinces(item["name"])
        #if "within" in item:
            #townland.within = item["within"]
        #if "within1" in item:
           # townland.within1 = item["within1"]

        # Set latitude and longitude if present in the item
        if "lat" in item and "long" in item:
            p.lat = item["lat"]
            p.long = item["long"]

        if "direction" in item:
            p.direction = item["direction"]
        if "PV_ID" in item:  # Check if CO_ID is in the item and map it to OSI_id
            p.OSI_id = item["PV_ID"]
        ps[item["name"]] = p


    return ps

def populate_province(onto):
    ps = get_Ireland_province_information(onto)

    Administrative_hierarchy_of_Ireland1 = onto.Administrative_hierarchy_of_Ireland1
    Administrative_hierarchy_of_Ireland2 = onto.Administrative_hierarchy_of_Ireland2
    Administrative_hierarchy_of_Ireland3 = onto.Administrative_hierarchy_of_Ireland3
    Administrative_hierarchy_of_Ireland4 = onto.Administrative_hierarchy_of_Ireland4
    Provinces = onto. Provinces
    part_of = onto.part_of
    lat = onto.lat
    long = onto.long
    level_in_hierarchy = onto.level_in_hierarchy
    ehInside = onto.ehInside

    with onto:
        for name, p in ps.items():
            current = Provinces(name, part_of=[Administrative_hierarchy_of_Ireland1, Administrative_hierarchy_of_Ireland2, Administrative_hierarchy_of_Ireland3, Administrative_hierarchy_of_Ireland4],
                                level_in_hierarchy=0)
            #if p.within:
                #arent_name = townland.within
                #parent_instance = onto[parent_name]
                #current.ehInside.append(parent_instance)
            #if townland.within1:
                #parent_name = townland.within1
                #parent_instance = onto[parent_name]
                #current.ehInside.append(parent_instance)

            latitude_value = p.lat
            longitude_value = p.long



            # Set the latitude and longitude properties to the district instance
            if hasattr(current, 'lat') and latitude_value is not None:
                current.lat = latitude_value
            if hasattr(current, 'long') and longitude_value is not None:
                current.long = longitude_value
            print(f"Latitude to be assigned: {latitude_value}")
            print(f"Longitude to be assigned: {longitude_value}")

            id = p.OSI_id
            if id is not None:
              current.OSI_id = id



            for bearing, values in p.direction.items():
                # note that: values is a dictionary: {'uri': uri, 'distance': distance}
                neighbour_name = values['name']
                neighbour = onto[neighbour_name]
                if bearing == "N":
                    current.nearest_N.append(neighbour)
                if bearing == "S":
                    current.nearest_S.append(neighbour)
                if bearing == "E":
                    current.nearest_E.append(neighbour)
                if bearing == "W":
                    current.nearest_W.append(neighbour)




# local_electoral_area

def get_Ireland_local_electoral_area_information(onto):
    local_electoral = dict()

    Local_Electoral_Areas = onto.Local_Electoral_Areas


    with open('dataset_id_cleaned/updated_local_electoral_cleaned.json', "r") as read_file:
        data = json.load(read_file)

    for item in data:
        local = Local_Electoral_Areas(item["name"]+"_area")
        if "within" in item:
            local.within = item["within"]
        if "direction" in item:
            local.direction = item["direction"]
            # Set latitude and longitude if present in the item
        if "lat" in item and "long" in item:
             local.lat = item["lat"]
             local.long = item["long"]
        if "LE_ID" in item:  # Check if CO_ID is in the item and map it to OSI_id
            local.OSI_id = item["LE_ID"]





        local_electoral[item["name"]] = local

    return local_electoral




def populate_Ireland_local_electoral(onto):
    local_electoral = get_Ireland_local_electoral_area_information(onto)

    Administrative_hierarchy_of_Ireland3 = onto.Administrative_hierarchy_of_Ireland3
    Local_Electoral_Areas = onto.Local_Electoral_Areas
    part_of = onto.part_of
    level_in_hierarchy = onto.level_in_hierarchy
    ehInside = onto.ehInside

    with onto:
        for name, local in local_electoral.items():
            current = Local_Electoral_Areas(name + "area", part_of=[Administrative_hierarchy_of_Ireland3], level_in_hierarchy=2)

            if local.within:
                #print(local.within)
                parent_name = local.within
                parent_instance = onto[parent_name]
                if parent_instance is not None:
                    current.ehInside.append(parent_instance)

            latitude_value = local.lat
            longitude_value = local.long

            # Print latitude and longitude values for debugging
            # print(f"Latitude for {uri}: {latitude_value}")
            # print(f"Longitude for {uri}: {longitude_value}")

            # Set the latitude and longitude properties to the district instance
            if latitude_value is not None:
                current.lat = latitude_value  # Assign directly, no append
            if longitude_value is not None:
                current.long = longitude_value  # Assign directly, no append

            id = local.OSI_id
            if id is not None:
                current.OSI_id = id

            for bearing, values in local.direction.items():

                neighbour_name = values['name'] + "area"
                neighbour = onto[neighbour_name]
                if neighbour is not None:
                    if bearing == "N":
                        current.nearest_N.append(neighbour)
                    if bearing == "S":
                        current.nearest_S.append(neighbour)
                    if bearing == "E":
                        current.nearest_E.append(neighbour)
                    if bearing == "W":
                        current.nearest_W.append(neighbour)


#electoral disision



def get_Ireland_electoral_division_information(onto):
    edivision = dict()

    Electoral_Division = onto.Electoral_Division

    with open('dataset_id_cleaned/edivi_cleaned.json', "r") as read_file:
        data = json.load(read_file)

    for item in data:
        elec = Electoral_Division(item["name"] + "_division")
        if "within" in item:
            elec.within = item["within"]
        if "direction" in item:
            elec.direction = item["direction"]

            # Set latitude and longitude if present in the item
        if "lat" in item and "long" in item:
            elec.lat = item["lat"]
            elec.long = item["long"]


        edivision[item["name"]] = elec

    return edivision


def populate_Ireland_electoral_division(onto):
    edivision = get_Ireland_electoral_division_information(onto)

    Administrative_hierarchy_of_Ireland4 = onto.Administrative_hierarchy_of_Ireland4
    Electoral_Division = onto.Electoral_Division
    part_of = onto.part_of
    level_in_hierarchy = onto.level_in_hierarchy
    ehInside = onto.ehInside
    lat = onto.lat
    long = onto.long


    with onto:
        for name, elec in edivision.items():
            current = Electoral_Division(name + "_division", part_of=[Administrative_hierarchy_of_Ireland4], level_in_hierarchy=2)

            if elec.within:
                parent_name = elec.within
                parent_instance = onto[parent_name]
                if parent_instance is not None:

                   current.ehInside.append(parent_instance)
            latitude_value = elec.lat
            longitude_value = elec.long

            # Print latitude and longitude values for debugging
            # print(f"Latitude for {uri}: {latitude_value}")
            # print(f"Longitude for {uri}: {longitude_value}")

            # Set the latitude and longitude properties to the district instance
            if latitude_value is not None:
                current.lat = latitude_value  # Assign directly, no append
            if longitude_value is not None:
                current.long = longitude_value  # Assign directly, no append

            for bearing, values in elec.direction.items():

                neighbour_name = values['name'] + "_division"
                neighbour = onto[neighbour_name]
                if neighbour is not None:
                    if bearing == "N":
                        current.nearest_N.append(neighbour)
                    if bearing == "S":
                        current.nearest_S.append(neighbour)
                    if bearing == "E":
                        current.nearest_E.append(neighbour)
                    if bearing == "W":
                        current.nearest_W.append(neighbour)






if __name__ == "__main__":
    onto = load_ontology()
    populate_province(onto)
    populate_Ireland_counties(onto)
    populate_Ireland_baronies(onto)
    populate_Ireland_district(onto)
    populate_Ireland_Civil_Parish(onto)
    populate_Ireland_local_electoral(onto)
    populate_Ireland_electoral_division(onto)
    populate_Ireland_townland(onto)

    onto.save('ontology_Ireland_Apr_2024.owl')



