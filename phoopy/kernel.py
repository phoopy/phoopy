import importlib
import sys
import re
from os import path
from .yaml_parser import YamlParser
from .container import Container


class Kernel(object):
    def __init__(self, environment, debug):
        self.__booted = False
        self.__bundles = None
        self.__environment = environment
        self.__debug = debug
        self.__config = {}
        self.__parameters = {}
        self.__container = None

    def get_environment(self):
        return self.__environment

    def boot(self):
        if self.__booted:
            return

        self.__initialize_configuration()

        self.__initialize_bundles()

        parser = YamlParser()

        services_buff = {}
        services_buff['services'] = self.__services

        for bundle_name in self.__bundles:
            bundle_services_path = self.__bundles[bundle_name].service_path()

            if bundle_services_path is not None:
                services_buff = parser.parse(
                    file_path=bundle_services_path,
                    result=services_buff
                )

        self.__services = services_buff['services']

        self.__init_container()

        self.__booted = True

    def __init_container(self):
        self.__container = Container()

        for service_name in self.__services:
            service_entry = self.__services[service_name]
            service_entry['key'] = service_name
            self.__create_dependency(service_entry)

    def __create_dependency(self, service_entry):
        class_instance = self.__import_module_variable(service_entry['class'])
        service_entry['class_instance'] = class_instance

        calls = service_entry.get('calls', [])
        args = service_entry.get('args', [])
        factory_method = service_entry.get('factory_method', None)
        kwargs = service_entry.get('kwargs', {})

        def _build_service(c):
            real_args = self.__process_args(args, c)
            real_kwargs = self.__process_kwargs(kwargs, c)
            if factory_method:
                factory_method_instance = getattr(class_instance, factory_method)
                object_instance = factory_method_instance(*real_args, **real_kwargs)
            else:
                object_instance = class_instance(*real_args, **real_kwargs)
            for call in calls:
                method = getattr(object_instance, call[0])
                method_args = self.__process_args(call[1].get('args', []), c)
                method_kwargs = self.__process_kwargs(call[1].get('kwargs', {}), c)
                method(*method_args, **method_kwargs)

            if 'command' in service_entry.get('tag', []):
                object_instance.project_path = self.get_root_dir()

            return object_instance

        tags = service_entry.get('tag', [])
        for tag_name in tags:
            tag_key = '{}.tag'.format(tag_name)
            if tag_key not in self.__container:
                self.__container[tag_key] = lambda c: []
            self.__container[tag_key].append(service_entry)

        self.__container[service_entry['key']] = _build_service

    def __process_args(self, args, c):
        return [self.__transform_magic_string(arg, c) for arg in args]

    def __process_kwargs(self, kwargs, c):
        return {
            key: self.__transform_magic_string(value, c)
            for (key, value) in kwargs.items()
        }

    def __transform_magic_string(self, value, c):
        const_matches = re.compile('^<const:([^>]+)>$').match(value)
        parameters_matches = re.compile('%[^%]+%').findall(value)

        if '@' == value[0]:
            return c[value[1:]]
        elif const_matches:
            return self.__import_module_variable(const_matches.groups(0)[0])
        elif parameters_matches:
            return self.__interpolate_parameter(value, parameters_matches)
        else:
            return value

    def __import_module_variable(self, path):
        path_pieces = path.split('.')
        if len(path_pieces) <= 1:
            raise Exception('Invalid path "{}". It should include module path'.format(path))
        module_path = '.'.join(path_pieces[0:-1])
        module_variable = path_pieces[-1]
        module_instance = importlib.import_module(module_path)
        if not hasattr(module_instance, module_variable):
            raise Exception('Module "{}" has no variable "{}"'.format(module_path, module_variable))
        return getattr(module_instance, module_variable)

    def __interpolate_parameter(self, value, matches):
        return_value = value

        for match in matches:
            match = match[1:-1]
            keys = match.split('.')
            parameter_value = self.__get_from_dict(keys, self.__parameters)
            if None is not parameter_value and not parameter_value:
                continue

            if isinstance(parameter_value, str):
                return_value = return_value.replace('%{}%'.format(match), parameter_value)
            else:
                return_value = parameter_value

        return return_value

    def __get_from_dict(self, keys, context):
        if keys[0] not in context:
            raise Exception('{} does not exists in parameters'.format(keys[0]))

        new_context = context[keys[0]]

        keys = keys[1:]
        if len(keys):
            return self.__get_from_dict(keys, new_context)

        return new_context

    def __initialize_configuration(self):
        config_path = path.join(self.get_app_dir(), 'config', 'config_{}.yml'.format(self.get_environment()))

        parser = YamlParser()
        self.__config = parser.parse(config_path)
        self.__services = self.__config['services']
        self.__parameters = self.__config['parameters']
        self.__parameters['kernel'] = {
            'root_path': self.get_root_dir(),
            'app_path': self.get_app_dir(),
            'var_path': self.get_var_dir(),
        }

    def __initialize_bundles(self):
        self.__bundles = {}

        for bundle in self.register_bundles():
            name = bundle.get_name()
            if name in self.__bundles.keys():
                raise Exception('Trying to register two bundles with the same name "{}"'.format(name))

            self.__bundles[name] = bundle

    def get_root_dir(self):
        return path.realpath(path.join(self.get_app_dir(), '..'))

    def get_app_dir(self):
        return path.dirname(path.realpath(sys.modules[self.__class__.__module__].__file__))

    def get_var_dir(self):
        return path.realpath(path.join(self.get_root_dir(), 'var'))

    def get_parameter(self, key):
        return self.__parameters[key]

    def get_container(self):
        return self.__container
