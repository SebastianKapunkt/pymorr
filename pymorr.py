import os

class Pymorr:
    def __init__(self):
        self.root = ""

    def set_root(self, input):
        """Sets the root path for all operations.
         Parameters
         ----------
            input : str
                a valid path to set as root
        """
        self.root = input
        print(self.root)

    def list_files_of_root(self):
        print('root' + self.root)
        if self.root:
            return os.listdir(self.root)
        else:
            return os.listdir()
