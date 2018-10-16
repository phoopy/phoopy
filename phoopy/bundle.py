from os import path
import sys


class Bundle(object):
    def __init__(self):
        pass

    def get_name(self):
        return self.__class__.__name__

    def get_bundle_dir(self):
        return path.dirname(path.realpath(sys.modules[self.__class__.__module__].__file__))

    def service_path(self):
        # return an yaml file path
        pass
