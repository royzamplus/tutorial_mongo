#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An example of how to get a Python handle to a MongoDB database """
import sys

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

    # Demonstrate the db.connection property to retrieve a reference to the
    # Connection object should it go out of scope. In most cases, keeping a 
    # reference to the Database object for the lifetime of your program
    # should be sufficient.

    assert dbh.connection == c
    print "Successfully set up a database handle"

    # A user document demonstrating one-to-many relationships using embedding
    user_doc = {
        "username":"foouser",
        "emails":[
            {
             "email":"foouser1@example.com",
             "primary":True
            },
            {
             "email":"foouser2@example2.com",
             "primary":False
            },
            {
             "email":"foouser3@example3.com",
             "primary":False
            }
        ]
    }

    # Insert the user document
    dbh.users.insert(user_doc, safe=True)
    # Retrieve the just-inserted document via one of its many email addresses
    user_doc_result = dbh.users.find_one({"emails.email":"foouser1@example.com"})

    # Naive method to remove an email address from a user document
    # Cumbersome and has a race condition
    user_doc = {
        "username":"foouser",
        "emails":[
            {
             "email":"foouser1@example.com",
             "primary":True
            },
            {
             "email":"foouser2@example2.com",
             "primary":False
            },
            {
             "email":"foouser3@example3.com",
             "primary":False
            }
        ]
    }
    # Insert the user document
    dbh.users.insert(user_doc, safe=True)
    # Retrieve the just-inserted document via username
    user_doc_result = dbh.users.find_one({"username":"foouser"})
    # Remove the "foouser2@example2.com" email address sub-document from the embedded list
    del user_doc_result["emails"][1]
    # Now write the new emails property to the database
    # May cause data to be lost due to the race between read and write
    dbh.users.update({"username":"foouser"},{"$set":{"emails":user_doc_result}},
        safe=True)

    # Atomically remove an email address from a user document race-free using the
    # $pull update modifier
    user_doc = {
        "username":"foouser",
        "emails":[
            {
             "email":"foouser1@example.com",
             "primary":True
            },
            {
             "email":"foouser2@example2.com",
             "primary":False
            },
            {
             "email":"foouser3@example3.com",
             "primary":False
            }
        ]
    }
    # Insert the user document
    dbh.users.insert(user_doc, safe=True)
    # Use $pull to atomically remove the "foouser2@example2.com" email sub-document
    dbh.users.update({"username":"foouser"},
        {"$pull":{"emails":{"email":"foouser2@example2.com"}}}, safe=True)

    # Use $pull to atomatically remove all email sub-documents with primary not equal to True
    dbh.users.update({"username":"foouser"},
        {"$pull":{"emails":{"primary":{"$ne":True}}}}, safe=True)

    # Use $push to atomically append a new email sub-document to the user document
    new_email = {"email":"fooemail4@exmaple4.com", "primary":False}
    dbh.users.update({"username":"foouser"},
        {"$push":{"emails":new_email}}, safe=True)

    # Demonstrate usage of the positional operator ($) to modify
    # matched sub-documents in-place.
    user_doc = {
        "username":"foouser",
        "emails":[
            {
             "email":"foouser1@example.com",
             "primary":True
            },
            {
             "email":"foouser2@example2.com",
             "primary":False
            },
            {
             "email":"foouser3@example3.com",
             "primary":False
            }
        ]
    }
    # Insert the user document
    dbh.users.insert(user_doc, safe=True)
    # Now make the "foouser2@example2.com" email address primrary
    dbh.users.update({"emails.email":"foouser2@example2.com"},
        {"$set":{"emails.$.primary":True}}, safe=True)
    # Now make the "foouser1@example.com" email address not primary
    dbh.users.update({"emails.email":"foouser1@example.com"},
        {"$set":{"emails.$.primary":False}}, safe=True)

if __name__ == '__main__':
    main()
