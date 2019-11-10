import glob
import json
import os


class Pymorr:
    def __init__(self):
        self.root = ""  # represents the root path for all operations
        self.supported_types = ('*.jpg', '*.png', '*.jpeg', '*.JPG')
        self.prefered_folder = {
            'Keep': 'keep',
            'Delete': 'delete',
            'Maybe': 'maybe'
        }
        self.image_index = 'index.json'

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
            files = os.listdir(self.root)
            list.sort(files)
            return files
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
        list.sort(files_grabbed)
        return files_grabbed

    def get_image_paths_from_log(self):
        """
        reads all image paths from log json

        Returns
        -------
        list of str
            paths of moved image files
        """
        image_index_path = os.path.join(self.root, self.image_index)
        image_log_paths = []
        if os.path.isfile(image_index_path):
            with open(image_index_path) as json_file:
                json_file_content = json.load(json_file)
                for item in json_file_content:
                    image_log_paths.append(item['path_after'])
        return image_log_paths

    def move_image(self, image, folder_to_move):
        """
        Moves an image to a desired folder under root and checks before
        if the folder exists. 'root/folder_to_move'
        Also adds the move to the log file 'index.json'.

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
        self.add_image_to_log(image, destination)
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
        Appends the data as json to the index.json.
        {
            "path_before": "path_before",
            "path_after": "path_after"
        }

        Parameters
        ----------
        path_before : str
            The full path before a change.

        path_after : str
            The full path after a change.
        """
        image_index_path = os.path.join(self.root, self.image_index)
        entry = {'path_before': path_before, 'path_after': path_after}
        if os.path.isfile(image_index_path):
            with open(image_index_path) as json_file:
                json_file_content = json.load(json_file)
            json_file_content.append(entry)
            with open(image_index_path, mode='w') as json_file:
                json_file.write(json.dumps(json_file_content, indent=2))
        else:
            new_json_array = []
            new_json_array.append(entry)
            with open(image_index_path, mode='w') as json_file:
                json_file.write(json.dumps(new_json_array, indent=2))

    def undo_last_move(self):
        """
        Looks up the last move in index.json and moves
        the file back to the location it was before (tracked by log).
        """
        image_index_path = os.path.join(self.root, self.image_index)
        with open(image_index_path, mode='r') as json_file:
            json_file_content = json.load(json_file)

        if len(json_file_content) > 0:
            image_to_move = json_file_content[len(json_file_content) - 1]
            path_after = image_to_move["path_after"]
            path_before = image_to_move["path_before"]

            json_file_content.pop(len(json_file_content) - 1)

            with open(image_index_path, mode='w') as json_file:
                json_file.write(json.dumps(json_file_content, indent=2))

            os.rename(path_after, path_before)
