import os
import glob

class Pymorr:
    def __init__(self):
        self.root = "" # represents the root path for all operations
        self.supported_types = ('*.jpg', '*.png', '*.jpeg')
        self.prefered_folder = {'Keep': 'keep', 'Delete': 'delete', 'Maybe': 'maybe'}

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

    def move_image_to_folder_under_root(self, image, folder_to_move):
        """
        Moves an image to a desired folder and checks before
        if the folder exists.

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
        return destination

    def create_if_not_exists(self, folder):
        """
        Checks if a disred folder under root exists and if not creates it.

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
