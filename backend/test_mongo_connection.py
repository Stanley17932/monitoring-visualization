from pymongo import MongoClient

# Replace with your actual MONGO_URI
MONGO_URI = "mongodb://127.0.0.1:27017/Visualization-metrics"

try:
    # Create a MongoDB client
    client = MongoClient(MONGO_URI)
    
    # Access the database
    db = client.get_database()  # This will use the database name from the URI
    print("Connected to MongoDB successfully!")
    
    # Print the database name
    print(f"Database Name: {db.name}")
    
    # List all collections in the database
    collections = db.list_collection_names()
    print("Collections:", collections)
    
    # Test querying a collection (e.g., metrics-data)
    if "metricsdata" in collections:
        print("Sample documents from 'metricsdata':")
        for doc in db["metricsdata"].find().limit(5):
            print(doc)
    else:
        print("'metricsdata' collection does not exist.")
except Exception as e:
    print("Failed to connect to MongoDB:", e)