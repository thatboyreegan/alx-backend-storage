#!/usr/bbin/env python3
"""this module will implement the  get_page function"""

import redis
import requests
from typing import Callable
from functools import wraps

cache = redis.Redis()


def count_urls(fn: Callable) -> Callable:
    """
    counts the number of times a url is requested

    Args:
        fn (Callable): Function to decorate
    Returns:
        Callable: function that counts the number of times
        a url is requested and returns the called function
    """
    @wraps(fn)
    def wrapper(url) -> str:
        cache.incr(f"count:{url}")
        cached_result = cache.get(f"cache:{url}")

        if cached_result:
            return cached_result.decode("utf-8")

        result = fn(url)
        cache.setex(f"cache:{url}", 10, result)
        return result
    return wrapper


@count_urls
def get_page(url: str) -> str:
    """
    gets the HTMLS content of a given url and returns it

    Args:
        url (str): url whose HTML content is suppsed to be returned
    Returns:
        str: the HTML content of the given url
    """
    r = requests.get(url)

    \return r.text
