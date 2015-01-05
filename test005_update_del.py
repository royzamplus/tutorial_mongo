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

    # First query to get a copy of the current document
    import copy
    old_user_doc = dbh.users.find_one({"username":"janedoe"})
    new_user_doc = copy.deepcopy(old_user_doc)
    # Modify the copy to change the email address
    new_user_doc["email"] = "janedoe74@example2.com"
    # Run the update query
    # Replace the matched document with the contents of new_user_doc
    dbh.users.update({"username":"janedoe"}, new_user_doc, safe=True)

    # Run the update query, using the $set update modifier.
    # We do not need to know the current contents of the document
    # with this approach, and so avoid an initial query and
    # potential race condition.
    dbh.users.update({"username":"janedoe"}, {"$set":{"email":"janedoe74@example2.com"}}, safe=True)

    # Update the email address and the score at the same time
    dbh.users.update({"username":"janedoe"}, {"$set":{"email":"janedoe74@example2.com", "score":1}}, safe=True)

    # Even if every document in your collection has a score of 0, 
    # Only the first matched document will have its "flagged" property set to True.
    dbh.users.update({"score":0}, {"$set":{"flagged":True}}, safe=True)

    # Once we supply the "multi=True" parameter, all matched documents will be updated.
    dbh.users.update({"score":0}, {"$set":{"flagged":True}}, multi=True, safe=True)

    # Delete all documents in user collection with score 1
    dbh.users.remove({"score":1}, safe=True)

    # Delete all documents in user collection
    dbh.users.remove(None, safe=True)

if __name__ == '__main__':
    main()
