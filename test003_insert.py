""" An example of how to insert a document """
import sys

from datetime import datetime
from pymongo import Connection
from pymongo.errors import ConnectionFailure

def main():
    """ Connect to MongoDB """
    try:
        c = Connection(host="localhost", port=27017)
        print "Connected successfully"
    except ConnectionFailre, e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)
    # Get a Database handle to a database named "mydb"
    dbh = c["mydb"]
    assert dbh.connection == c

    user_doc = {
        "username" : "janedoe",
        "firstname" : "Jane",
        "surname" : "Doe",
        "dateofbirth" : datetime(1974, 4, 12),
        "email" : "janedoe@example.com",
        "score" : 0
    }

    # safe=True ensures that your write
    # will succeed or an exception will be thrown
    dbh.users.insert(user_doc, safe=True)
    print "Successfully inserted document: %s" % user_doc

if __name__ == '__main__':
    main()
