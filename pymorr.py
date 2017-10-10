import os
import glob

class Pymorr:
    def __init__(self):
        self.root = "" # represents the root path for all operations
        self.supported_types = ('*.jpg', '*.png', '*.jpeg')
        self.prefered_folder = {'Keep': 'keep', 'Delete': 'delete', 'Maybe': 'maybe'}
        self.image_index = 'index.txt'

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

    def get_image_paths_from_root(self):
        """
        Finds all image paths from the root path

        Returns
        -------
        list of str
            path of image files with root path
        """
        files_grabbed = []
        for files in self.supported_types:
            files_grabbed.extend(glob.glob(os.path.join(self.root, files)))
        return files_grabbed

    def move_image(self, image, folder_to_move):
        """
        Moves an image to a desired folder under root and checks before
        if the folder exists. 'root/folder_to_move'
        Also adds the move to the log file 'index.txt'. 

        Parameters
        ----------
        image : str
            Full path of an image.

        folder_to_move : str
            Just folder name that already exists under root.
            Will be used as 'root/folder_to_move'.
            Should be used with 'preffered_folder'.

        Returns
        -------
        str
            Full path of the image after move.
        """
        directory = self.create_if_not_exists(folder_to_move)
        destination = os.path.join(directory, os.path.basename(image))
        os.rename(image, os.path.join(image, destination))
        self.add_image_to_log(image,destination)
        return destination

    def create_if_not_exists(self, folder):
        """
        Checks if a desired folder under root exists and if not creates it.

        Parameters
        ----------
        folder : str
            Folder name. Will be used as root/folder

        Returns
        -------
        str
            Full path of folder to check.
        """
        directory = os.path.join(self.root, folder)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def add_image_to_log(self, path_before, path_after):
        """
        Appends two paths to the bottom of a file.

        Parameters
        ----------
        path_before : str
            The full path before a change.

        path_after : str
            The full path after a change.
        """
        image_index_path = os.path.join(self.root,self.image_index)

        if os.path.isfile(image_index_path):
            with open(image_index_path, "a") as myfile:
                myfile.write("\n'{}','{}'".format(path_before, path_after))
        else:
            with open(image_index_path, "a") as myfile:
                myfile.write("'{}','{}'".format(path_before, path_after))
