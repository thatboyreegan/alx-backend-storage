#!/usr/bin/env python3
"""
this module has a function that returns a list of schools having a given topic
"""


def schools_by_topic(mongo_collection, topic):
    """returns the list of school having a specific topic.

    Args:
        mongo_collection (Collection): collection to query into.
        topic (str): topic to search for.

    Returns:
        Cursor: cursor object of the documents containing the given topic.
    """
    return mongo_collection.find({"topics": topic})
