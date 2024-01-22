from pymongo import MongoClient
def get_database():
   CONNECTION_STRING = "mongodb+srv://homescanpropertyapp:5kXsoJbXxQ5ymRhw@homescan.18gfa1r.mongodb.net/?retryWrites=true&w=majority"
   client = MongoClient(CONNECTION_STRING)
   return client['property']
  