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

    dbh.users.insert(user_doc)
    # If we place an index on property "emails.email",
    # e.g. dbh.users.create_index("emails.email")
    # this find_one query can use a btree index
    user = dbh.users.find_one({"emails.email":"foouser2@example2.com"})

    # Create index on username property
    dbh.users.create_index("username")

    # Create a compound index on first_name and last_name properties
    # with ascending index direction
    dbh.users.create_index([("first_name", pymongo.ASCENDING), ("last_name", pymongo.ASCENDING)])

    # Create a compound index called "name_idx" on first_name and last_name properties
    # with ascending index direction
    dbh.users.create_index([
        ("first_name", pymongo.ASCENDING),
        ("last_name", pymongo.ASCENDING)
        ],
        name="name_idx")

    # Create index in the background
    # Database remains usable
    dbh.users.create_index("username", background=True)

    # Create index with unique constraint on username property
    dbh.users.create_index("username", unique=True)

    # Create index with unique constraint on username property
    # instructing MongoDB to drop all duplicates after the first document it finds.
    dbh.users.create_index("username", unique=True, drop_dups=True)
    # Could equally be written:
    # dbh.users.create_index("username", unique=True, dropDups=True)

    # Create index on username property called "username_idx"
    dbh.users.create_index("username", name="username_idx")
    # Delete index called "username_idx"
    dbh.users.drop_index("username_idx")

    # Create a compound index on first_name and last_name properties
    # with ascending index direction
    dbh.users.create_index([("first_name", pymongo.ASCENDING), ("last_name", 
    pymongo.ASCENDING)])
    # Delete this index
    dbh.users.drop_index([("first_name", pymongo.ASCENDING), ("last_name", 
    pymongo.ASCENDING)])

if __name__ == '__main__':
    main()
