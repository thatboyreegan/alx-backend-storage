#!/usr/bin/env python3
"""
this module contains a function inserts a new document in a collection
based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a new documents in a collection based on kwargs

    Args:
        mongo_collection (collection): the collcetion to insert into

    Returns:
        new _id
    """
    if kwargs:
        insert_document = mongo_collection.insert_one(kwargs)
        return insert_document.inserted_id
    else:
        return ""
