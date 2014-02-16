from os.path import expanduser


class Config():

    def __init__(self):
        home = expanduser("~")
        print home