import pyodbc
from pymongo import MongoClient
import json
import codecs


# Connecting to Locally saved Access Database 
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Erevos\Desktop\Reviews.accdb;')
cursor = conn.cursor()

cursor.execute("Select * from reviews")

# Creating List to add all the reviews from the database and then appending them into the ReviewsList.
ReviewsList = []
for row in cursor.fetchall():
    ReviewsList.append(row)


# Specifing the columns needed.
keys = ("ID", "County", "User", "Review","Date", "Shop", "Stars", "dcstars")

# Matching columns with the values
JsonDict = [dict(zip(keys, item)) for item in ReviewsList]

# Saving the new structured data into a json file and now the file is ready to 
# be uploaded in Cloud Database (MONGODB)
with codecs.open('Data.json', 'w', encoding= 'utf8') as jsondata:
    json.dump(JsonDict, jsondata, indent=2, sort_keys = True, ensure_ascii=False)



