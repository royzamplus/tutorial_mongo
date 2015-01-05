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

    # Find a single document with the username "janedoe".
    user_doc = dbh.users.find_one({"username":"janedoe" })
    if not user_doc:
        print "no document found for username janedoe"
    
    # Find all documents with the firstname "jane".
    # Then iterate through them and print out the email address.
    users = dbh.users.find({"firstname":"Jane"})
    for user in users:
        print user.get("email")

    # Only retrieve the "email" field from each matching document.
    users = dbh.users.find({"firstname":"Jane"}, {"email":1})

    # Find out how many documents are in users collection, efficiently
    userscount = dbh.users.find().count()
    print "There are %d documents in users collection" % userscount

    # Return all user with firstname "jane" sorted
    # in descending order by birthdate (ie youngest first)
    users = dbh.users.find(
        {"firstname":"Jane"}).sort(("dateofbirth", pymongo.DESCENDING))

    users = dbh.users.find({"firstname":"Jane"}, sort=[("dateofbirth", pymongo.DESCENDING)])

    # Return at most 10 users sorted by score in descending order
    # This may be used as a "top 10 users highscore table"
    users = dbh.users.find().sort(("score", pymongo.DESCENDING)).limit(10)
    for user in users:
        print user.get("username"), user.get("score", 0)

    # Traverse the entire users collection, employing Snapshot Mode
    # to eliminate potential duplicate results.
    for user in dbh.users.find(snapshot=True):
        print user.get("username"), user.get("score", 0)

if __name__ == '__main__':
    main()
