from pymongo import MongoClient

def get_database():
    CONNECTION = "mongodb+srv://super:super@maincluster.tt6dyyu.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION)

    return client['BitcoinPayroll']

if __name__ == "__main__":
    dbname = get_database()
