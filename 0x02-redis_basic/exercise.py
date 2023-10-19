#!/usr/bin/env python3
"""the CACHE module"""

import redis
from functools import wraps
from typing import Callable, Optional, Union, Any
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """counts how many times methods of the Cache class are called.

    Args:
        method (Callable): method being called.

    Returns:
        Callable: Wrapper function that increments the count and returns
            the called method.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Callable:
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """stores the history of inputs and outputs of a particular method.

    Args:
        method (Callable): method being called.

    Returns:
        Callable: Wrapper function that pushes the inputs and outputs
            to their respective lists and returns output of the method.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", str(output))

        return output

    return wrapper


class Cache:
    """The Cache class"""

    def __init__(self) -> None:
        """Initializes a new instance of the class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, float, bytes]) -> str:
        """
        takes a dtata argument and returns a string

        Args:
            data (Union[str, int ,float, bytes]): data to e stored in redis
        Returns:
            str: a string representation of the generated uuid4
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Any:
        """gets a value based on the key from the Redis server.

        Args:
            key (str): Key of the value to get.
            fn (Optional[Callable]): Callable to convert the
                value to required format.

        Returns:
            Any: Value in the desired format, bytes if `fn` is not provided and
                `None` if the key is not found.
        """
        value = self._redis.get(key)

        if fn:
            value = fn(value)

        return value

    def get_int(self, key: str) -> Optional[int]:
        """gets an integer value.

        Args:
            key (str): Key of the value to get.

        Returns:
            int: Value as an integer or None if key is not found.
        """
        return self.get(key, int)

    def get_str(self, key: str) -> Optional[str]:
        """gets string value.

        Args:
            key (str):Key of the value to get.

        Returns:
            str: Value as a str or None if key is not found.
        """
        return self.get(key, str)


def replay(fn: Any) -> None:
    """displays history of calls of a particular function.

    Args:
        fn (Any): Function to display its history.
    """

    rs = fn.__self__._redis
    name = fn.__qualname__

    count = int(rs.get(name))
    print("{} was called {} times:".format(name, count))

    for input, output in zip(
        rs.lrange(f"{name}:inputs", 0, -1), rs.lrange(f"{name}:outputs", 0, -1)
    ):
        print(
            "{}(*{}) -> {}".format(
                name, input.decode("utf-8"), output.decode("utf-8")
            )
        )
