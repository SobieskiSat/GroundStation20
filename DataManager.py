import yaml
import os
class Data

class DataManager:
    def __init__(self, dir = 'readings/', file_name = 'reading', max = 500):
        self.data = []

class MemoryManager:
    def __init__(self):
        self.conf = ConfigData()
        self.mem = Memory()
        self.__all = (self.conf, self.mem)

    def __getitem__(self, key):
        for d in self.__all:
            if key in d:
                return d[key]

class DynamicMemory:
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        print(self.data)
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __contains__(self, key):
        return key in self.data

class ConfigData:
    def __init__(self, file = None, default_file = None):
        self.default_file = default_file
        self.file_dir = file
        self.conf = {}
        self.read_config()

    def __getitem__(self, key):
        return self.conf[key]

    def __setitem__(self, key, value):
        self.conf[key] = value
        self.write_config()

    def write_config(self):
        if self.file_dir:
            try:
                with open(self.file_dir, 'w') as yamlfile:
                    yaml.dump(self.conf, yamlfile)
            except Exception as e:
                print('Could not save conf', e)

    def read_config(self):
        if self.file_dir:
            try:
                with open(self.file_dir, 'r') as yamlfile:
                    self.conf.update(yaml.load(yamlfile))
                return self.conf
            except Exception as e:
                print('Could not load conf', e)

        if self.default_file:
            try:
                with open(self.default_file, 'r') as yamlfile:
                    self.conf.update(yaml.load(yamlfile))
                return self.conf
            except Exception as e:
                print('Could not load default conf', e)

    def change_file(self, file):
        self.file_dir = file
        self.read_config()

    def __contains__(self, key):
        return key in self.conf

dm = DataManager()
dm.conf.change_file('test2.yml')
print(dm['xd'])
