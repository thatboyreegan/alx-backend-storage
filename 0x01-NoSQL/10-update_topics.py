#!/usr/bin/env python3
"""
this module has a function that changes all topics of a school
document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on name

    Args:
        mongo_collection (collection): collection to make changes in
        name (str): school name to update
        topics (str): topics to change
    Returns:
        None
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
