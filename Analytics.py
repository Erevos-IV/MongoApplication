# Import libraries.
import json
from pymongo import *
import folium
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


# Connect to the database.
client = MongoClient("mongodb+srv://bill:bill@clusterreviews.eb583st.mongodb.net/?retryWrites=true&w=majority")
db = client['Review']
collection = db['reviews']

# Aggregations
Average_Stars_Per_Shop = [
    {
        "$group": {
            "_id": { "Shop": "$Shop", "County": "$County" },
            "avgStars": { "$avg": "$Stars" }
        }
    }
]

popular_shops = collection.aggregate([
    {"$group": {"_id": {"Shop":"$Shop", "County":"$County"}, "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
])


# Find Areas per shop to create map
reviews_by_county = list(collection.aggregate([
    {"$group": {"_id": "$County_en", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]))

#-----------------------------------------------------

# Functions / Analytics
def Create_hitmap(reviews_by_county):
    map = folium.Map(location=[35, 25], zoom_start=5)
    geolocator = Nominatim(user_agent="geoapi", timeout=30) 
    # Iterate over the reviews_by_county and add a marker to the map for each county:    
    for county in reviews_by_county:
        location = geolocator.geocode(county['_id'])
        if location:
            folium.Marker(location=[location.latitude, location.longitude],
                                    popup=county['_id'] + ': ' + str(county['count'])).add_to(map)
        else:
            print(f"{county['_id']} not found") 
            
    
    map.save("map.html")


def find_average_stars_per_shop_per_county(pipeline):
    result = collection.aggregate(pipeline)
    results = list(result)
    return result

# Find the shops with most reviews in Descending mode.
def Find_Top_Shops_Descending(shop):
    for shop in popular_shops:
        print(shop)


# This function will add all the records, given the list and the collection, to the cloud database
def insert_analyzed_records(list_of_data, collection_name):
    To_Be_inserted_collection = db[collection_name]
    To_Be_inserted_collection.insert_many(list_of_data)



### SEABORN
# Retrieve data from MongoDB
#data = list(collection.find())

# Convert data to DataFrame
#df = pd.DataFrame(data)
#print(df.head())
# get the geolocation information
#geolocator = Nominatim(user_agent="geoapiExercises")



#for i in range(len(df)):
#    location = df.iloc[i]['County_en'] + ', Greece'
#    try:
#        coord = geolocator.geocode(location)
#        df.at[i,'lat'] = coord.latitude
#        df.at[i,'lon'] = coord.longitude
#    except GeocoderTimedOut as e:
#        print(f"Error: Geocoder Timed Out")


  

# Create heatmap

#sns.heatmap(df, x='lon', y='lat', cmap='YlGnBu')











# -----------------------------------TESTING FOLLOWS----------------------------------------------
#geolocator = Nominatim(user_agent="geoapi", timeout=30)
#county_names = ["Athens", "Thessaloniki", "Heraklion", "Patras", "Larisa"]
#for county in county_names:
#    location = geolocator.geocode(county)
#    if location:
#        print(county, ":", location.latitude, location.longitude)
#    else:
#        print(county, "not found")



# Update the documents to have county in English too
#result = collection.update_many(
#    {"County": "Κοζάνη"},
#    {"$set": {"County_en": "Kozani"}})


#counties = collection.distinct("County")
#counties = list(collection.aggregate([{"$group":{"_id":"$County"}},{"$sort":{"_id":1}}]))
#print(counties)