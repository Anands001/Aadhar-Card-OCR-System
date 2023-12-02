import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

db = myclient["OCR"]

# print(myclient.list_database_names())
collection = db['aadhar_info']


def store_aadhar_info(aadhar_data):
    try:

        # Store Aadhar information in MongoDB
        result = collection.insert_one(aadhar_data)
        # display()
        return {"success": True, "message": "Aadhar information stored successfully",
                "inserted_id": str(result.inserted_id)}

    except Exception as e:
        return {"success": False, "message": f"Error storing Aadhar information: {str(e)}"}


def display():
    cursor = collection.find()

    for document in cursor:
        print(document)