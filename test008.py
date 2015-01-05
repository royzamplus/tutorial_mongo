#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    # location property is an array with x,y ordering
    user_doc = {
        "username":"foouser",
        "user_location":[x,y]
    }
    # location property is an array with y,x ordering
    user_doc = {
        "username":"foouser",
        "user_location":[y,x]
    }
    import bson
    # location property is a sub-document with y,x ordering
    loc = bson.SON()
    loc["y"] = y
    loc["x"] = x
    user_doc = {
        "username":"foouser",
        "user_location":loc
    }
    import bson
    # location property is a sub-document with x,y ordering
    loc = bson.SON()
    loc["x"] = x
    loc["y"] = y
    user_doc = {
        "username":"foouser",
        "user_location":loc
    }

    # Create geospatial index on "user_location" property.
    dbh.users.create_index([("user_location", pymongo.GEO2D)])

    # Create geospatial index on "user_location" property.
    dbh.users.create_index([("user_location", pymongo.GEO2D), ("username", pymongo.ASCENDING)])

    # Find the 10 users nearest to the point 40, 40 with max distance 5 degrees
    nearest_users = dbh.users.find(
        {"user_location":
            {"$near" : [40, 40],
             "$maxDistance" : 5}}).limit(10)
    # Print the users
    for user in nearest_users:
        # assume user_location property is array x, y
        print "User %s is at location %s, %s" % (user["username"], user["user_location"][0],
            user["user_location"][1])

    box = [[50.73083, -83.99756], [50.741404,  -83.988135]]
    users_in_boundary = dbh.users.find({"user_location":{"$within": {"$box":box}}})

    users_in_circle = dbh.users.find({"user_location":{"$within":{"$center":[40, 40, 5]}}}).limit(10)

    # Find the 10 users nearest to the point 40, 40 with max distance 5 degrees
    # Uses the spherical model provided by MongoDB 1.8.x and up
    earth_radius_km = 6371.0
    max_distance_km = 5.0
    max_distance_radians = max_distance_km / earth_radius_km
    nearest_users = dbh.users.find(
        {"user_location":
            {"$nearSphere" : [40, 40],
             "$maxDistance":max_distance_radians}}).limit(10)
    # Print the users
    for user in nearest_users:
        # assume user_location property is array x,y
        print "User %s is at location %s,%s" %(user["username"], user["user_location"][0],
            user["user_location"[1])

if __name__ == '__main__':
    main()
