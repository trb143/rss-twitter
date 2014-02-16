import yaml


class YamlReader():

    def __init__(self):
        pass

    def read_file(self, file_path):
        try:
            data = open(file_path, 'r')
            self.data = yaml.load(data)
            data.close()
        except :
            print"oops"
