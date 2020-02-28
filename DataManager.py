import yaml
import os
import time


class DataManager:
    def __init__(self, dir = 'readings/', file_name = 'reading', max = 500):
        self.data = []
        self.max = max
        self.dir = dir
        self.data_processor = DataProcessor()
        #Check if directry exists, if not create it
        if not os.path.isdir(dir):
            try:
                os.mkdir(dir)
            except Exception as e:
                print('[DM] mkdir:', e)
        self.file_name_prefix = file_name
        self.obtain_file_num()
        self.file = open(self.file_dir, 'a+')

    @property
    def file_dir(self):
        return self.dir+self.file_name_prefix+'_'+str(self.file_num)+'.txt'

    def obtain_file_num(self):
        self.file_num = 1
        while os.path.isfile(self.file_dir):
            self.file_num += 1

    def append(self, value):
        timestamp = time.time()
        if len(self.data) >= self.max:
            self.data.pop(0)
        try:
            new_data = str(timestamp)+'_'+str(value)
            new_data = self.data_processor.interpreter(new_data)
        except Exception as e:
            print('[DM]', e)

        self.data.append({'time':timestamp, 'raw':value, 'processed':new_data})
        self.__write_data('{}@{}\n'.format(timestamp, value))
        return new_data

    def __write_data(self, data):
        self.file.write(data)
        self.file.flush()
        os.fsync(self.file.fileno())

    def __del__(self):
        os.fsync(self.file.fileno())
        try:
            self.file.close()
        except Exception as e:
            print('[DM]', e)

    def get_last(self, num = 100):
        return self.data[-num:]

    def new_data_arranger(self, *attr):
        class DataArranger:
            def __init__(self, df, names):
                self.data_func = df
                self.names = names

            def get_data(self, num = 100):
                data = self.data_func(num)
                ans = []
                for n in self.names:
                    new = []
                    for d in data:
                        new.append(d['processed'][n])
                    ans.append(new)
                return ans
        da = DataArranger(self.get_last, attr)
        return da.get_data



class DataProcessor:
    def __init__(self):
        self.structure = None

    def set_structure(self, structure):
        self.structure = structure

    def interpreter_old(self, data):
        if not self.structure:
            return {}
        #structure=('time','rssi','x','y', 'h', 'temperature', 'pressure', 'pm25', 'pm10')
        new_data = data.split('_')
        new_data = list(map(float, new_data))
        structure = self.structure
        return dict(zip(structure, new_data))

    def interpreter(self, data):
        ans = {}
        while data != '':
            big_c = str(data[0]).upper()
            res, data = (data[1:]).split(big_c)
            if big_c in self.structure:
                ans[self.structure[big_c]] = res
        return ans

class MemoryManager:
    def __init__(self):
        self.conf = ConfigData('config.yaml')
        self.dyn = DynamicMemory()
        self.dm = DataManager()
        self.__all = (self.conf, self.dyn)

    def __getitem__(self, key):
        for d in self.__all:
            if key in d:
                return d[key]

class DynamicMemory:
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        #print(self.data)
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
                print('[CONF]Could not save conf', e)

    def read_config(self):
        if self.file_dir:
            try:
                with open(self.file_dir, 'r') as yamlfile:
                    self.conf.update(yaml.load(yamlfile))
                return self.conf
            except Exception as e:
                print('[CONF]Could not load conf', e)

        if self.default_file:
            try:
                with open(self.default_file, 'r') as yamlfile:
                    self.conf.update(yaml.load(yamlfile))
                return self.conf
            except Exception as e:
                print('[CONF]Could not load default conf', e)

    def change_file(self, file):
        self.file_dir = file
        self.read_config()

    def __contains__(self, key):
        return key in self.conf
'''
dp = DataProcessor()
dp.set_structure({'T':'temperature', 'P':'pressure'})
print(dp.interpreter('t12Tp17P'))
'''
