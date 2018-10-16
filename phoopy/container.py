# -*- coding: utf-8 -*-


class ContainerException(Exception):
    pass


class Container(object):
    def __init__(self, values=None):
        self.__factories = {}
        self.__cache = {}

    def __setitem__(self, key, item):
        self.__factories[key] = item
        if key in self.__cache:
            del self.__cache[key]

    def __getitem__(self, key):
        self.__assert_dependency_exists(key)
        if key not in self.__cache:
            self.__cache[key] = self.__factories[key](self)
        return self.__cache[key]

    def __delitem__(self, key):
        self.__assert_dependency_exists(key)
        del self.__factories[key]
        del self.__cache[key]

    def __contains__(self, key):
        return key in self.__factories

    def keys(self):
        return self.__factories.keys()

    def get(self, key):
        return self.__getitem__(key)

    def __assert_dependency_exists(self, key):
        if key not in self.__factories:
            raise ContainerException('Dependency {} is not declared'.format(key))
