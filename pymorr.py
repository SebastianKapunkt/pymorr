import os
import glob

class Pymorr:
    def __init__(self):
        self.root = "" # represents the root path for all operations
        self.supported_types = ('*.jpg', '*.png', '*.jpeg')

    def set_root(self, input):
        """
        Sets the root path for all operations.

        Parameters
        ----------
            input : str
                a valid path to set as root
        """
        self.root = input
        print(self.root)

    def list_files_of_root(self):
        """Prints all files that are in the directory of root"""
        print('root' + self.root)
        if self.root:
            return os.listdir(self.root)
        else:
            return os.listdir()

    def get_images_of_root(self):
        """
        finds all images of root path

        Returns
        -------
        list of str
            path of image files with root path
        """
        files_grabbed = []
        for files in self.supported_types:
            files_grabbed.extend(glob.glob(os.path.join(self.root, files)))
        return files_grabbed
