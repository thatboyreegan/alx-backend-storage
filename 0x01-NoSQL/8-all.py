#!/usr/bin/env python3
"""this module contains function that lists all documents in a collection"""


def list_all(mongo_collection):
    """
    this function lists all documents in a collection

    Args:
        mongo_collection (collection): collection whose documents should be
        listed
    Returns:
        a list of all documents or an empty list if there is no document
    """

    collection = mongo_collection.find()

    return collection
