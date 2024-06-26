from pymongo.mongo_client import MongoClient

"""
MOVE TO ENV FILE
"""
username = "manugasemmanuell"
password = "jrBPFS2kN8NbdrWN"

uri = f"mongodb+srv://{username}:{password}@devcluster.wnkgfny.mongodb.net/?appName=DevCluster"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.TimeCapsuleDB
time_capsules_collection = db.timecapsules
users_collection = db.users