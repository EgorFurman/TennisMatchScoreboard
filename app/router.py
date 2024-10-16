import re
from typing import Callable

from app.exceptions import MethodNotAllowed, PathNotFoundError


class Router:
    _routes = {
        'GET': {},
        'POST': {}
    }

    @classmethod
    def route(cls, path: str, method: str = 'GET'):
        def register_route(handler: Callable):
            cls._routes[method][path] = handler
            return handler

        return register_route

    @classmethod
    def resolve(cls, path: str, method: str = 'GET'):
        if method not in cls._routes:
            raise MethodNotAllowed(method)

        try:
            return cls._routes[method][path]
        except KeyError:
            raise PathNotFoundError(path)




    # @classmethod
    # def route(cls, path: str, method: str = 'GET'):
    #     def inner(handler: Callable):
    #         cls._router[method][path] = handler
    #         return handler
    #     return inner

    # @classmethod
    # def resolve(cls):
    #     pass