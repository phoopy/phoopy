import yaml
from os import path


class YamlParser(object):
    def parse(self, file_path, result=None):
        if not path.exists(file_path):
            raise Exception('File {} does not exists'.format(file_path))

        data_buffer = yaml.load(open(file_path, 'r').read())

        result = {} if result is None else result
        for key in data_buffer:
            if 'imports' == key:
                for entry in data_buffer[key]:
                    resource_path = path.join(path.dirname(file_path), entry['resource'])
                    self.merge(result, self.parse(resource_path))
            else:
                to_merge = {}
                to_merge[key] = data_buffer[key]
                self.merge(result, to_merge)

        return result

    def merge(self, destination, source):
        """
        run me with nosetests --with-doctest file.py

        >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
        >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
        >>> merge(a, b) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
        """
        for key, value in source.items():
            if isinstance(value, dict):
                # get node or create one
                node = destination.setdefault(key, {})
                if node is not None:
                    self.merge(node, value)
                else:
                    destination[key] = value
            else:
                destination[key] = value
