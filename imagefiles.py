from random import shuffle
from abc import ABCMeta, abstractmethod

import os

import shutil


class ImageFiles(metaclass=ABCMeta):
    # Id for the out image generated
    # this should be shared from objects from different
    # classes
    image_id = None

    # Stat structure set for the whole project
    stats = {}

    # Output path and suffixes
    _output_folder = None

    # List of Mushafs
    _mushafs = []

    #################################
    #
    # Constructor
    #
    #################################

    def __init__(self):
        """
        The base class with the functionality used by all Mushaf
        to generate the train, validate, and test images
        """
        self._group_id = None
        self._shuffled_image_groups = []

        # Setup the stats for this Mushaf
        if 'summary' not in ImageFiles.stats:
            ImageFiles.stats['summary'] = [0] * len(self.image_groups)
        ImageFiles.stats[self.mushaf_group_name] = [0] * len(self.image_groups)

    #################################
    #
    # Instance methods
    #
    #################################

    def get_copy_list(self, out_path_suffix, count=1, generate_id=True):
        """
        Generate the output path of an image and
        append the suffix to the output path

        :param generate_id:
        :param count: Number of image file paths to generate
        :param out_path_suffix: is this output for test, validate, or test
        """

        copy_list = []
        for i in range(count):
            group_id = self.get_group_id()

            # get image name from shuffled list
            image_file_name = self.get_shuffled_image_name(group_id)

            # get full path of destination for image
            image_dest_path = self.get_dest_path(group_id, image_file_name, out_path_suffix, generate_id)

            # get the source path
            image_source_path = os.path.join(self.image_base_folder, image_file_name)

            # append to output list
            copy_list.append([image_source_path, image_dest_path])

            # update stats
            ImageFiles.stats['summary'][group_id] += 1
            ImageFiles.stats[self.mushaf_group_name][group_id] += 1

        return copy_list

    def get_shuffled_image_name(self, group_id):
        shuffled_image_group = self._shuffled_image_groups[group_id]
        image_file_name = self.get_image_file_name(shuffled_image_group.pop())
        return image_file_name

    def get_dest_path(self, group_id, image_file_name, out_path_suffix,
                      generate_id=True):

        if generate_id:
            image_id_str = str(ImageFiles.get_out_image_id()).zfill(4)

            # get image output path
            image_dest_path = '{0}_G{1}_{2}_{3}'.format(image_id_str, str(group_id).zfill(2), self.mushaf_group_name,
                                                        image_file_name)
        else:
            # get image output path
            image_dest_path = 'G{0}_{1}_{2}'.format(str(group_id).zfill(2), self.mushaf_group_name,
                                                    image_file_name)

        image_dest_path = os.path.join(ImageFiles._output_folder, out_path_suffix, image_dest_path)
        return image_dest_path

    def get_group_id(self):
        """
        Which group to select the image from
        """
        if self._group_id is None:
            self._group_id = 0
        else:
            self._group_id = (self._group_id + 1) % len(self.image_groups)

        return self._group_id

    def generate_group(self, shuffle_group=True):

        # Always reset shuffled image groups
        self._shuffled_image_groups = []

        # Iterate over image groups and generate image groups (shuffled if needed)
        for image_group in self.image_groups:
            shuffled_image_group = list(range(image_group[0], image_group[1]))
            if shuffle_group:
                shuffle(shuffled_image_group)
            self._shuffled_image_groups.append(shuffled_image_group)

    #################################
    #
    # Static methods
    #
    #################################

    @staticmethod
    def get_out_image_id():
        """
        Get the global id of the image file
        """
        if ImageFiles.image_id is None:
            ImageFiles.image_id = 0
        else:
            ImageFiles.image_id += 1

        return ImageFiles.image_id

    @staticmethod
    def set_output_path(output_folder: str, out_suffixes: list = None):
        ImageFiles._output_folder = output_folder

        # Create sub folders in output_folder if they don't exist
        if out_suffixes:
            for out_suffix in out_suffixes:
                out_path = os.path.join(ImageFiles._output_folder, out_suffix)
                if not os.path.exists(out_path):
                    os.mkdir(out_path)

    @staticmethod
    def add_mushaf(mushaf):
        """
        Add mushaf to the list of supported

        :type mushaf: Mushaf to be added
        """
        ImageFiles._mushafs.append(mushaf)

    @staticmethod
    def generate_groups(shuffle_group=True):

        # Iterate over mushafs and generate groups (shuffled or not)
        for mushaf in ImageFiles._mushafs:
            mushaf.generate_group(shuffle_group)

    @staticmethod
    def all_copy_list(out_path_suffix, count=1, new_shuffle_groups=False,
                      generate_id=True, round_up=True):

        """
        Generate the copy list for all mushafs added to ImageFiles

        :param new_shuffle_groups:
        :param round_up: True=round up, False don't round
        :param out_path_suffix:
        :param count:
        :param generate_id:
        :return:
        """
        copy_list = []

        # Count per mushaf and make it balanced across mushaf and groups
        mushafs_count = len(ImageFiles._mushafs)
        groups_count = mushafs_count * len(ImageFiles._mushafs[0].image_groups)
        count_per_mushaf = int(count / groups_count)
        count_pre_mushaf_mod = count % groups_count

        # Only round up when requested
        if round_up:
            reminder = 0 if count_pre_mushaf_mod == 0 else 1
        else:
            reminder = 0

        # Set the count per-mushaf to be a multiple of groups_count
        count_per_mushaf = (count_per_mushaf + reminder) * groups_count

        # Generate new shuffle groups if needed
        if new_shuffle_groups:
            ImageFiles.generate_groups(shuffle_group=True)

        # Loop over all mushafs registered
        for mushaf in ImageFiles._mushafs:

            # Get copy list
            mushaf_copy_list = mushaf.get_copy_list(out_path_suffix, count_per_mushaf, generate_id=False)

            # Concat copy lists
            copy_list = copy_list + mushaf_copy_list

        # Shuffle the new copy_list
        shuffle(copy_list)

        # Add index to the output files
        if generate_id:
            for index, copy_item in enumerate(copy_list):
                # Get filename from out path
                path, filename = os.path.split(copy_item[1])

                # Add index to destination file name
                filename = str(index).zfill(4) + '_' + filename

                # Rejoin path and filename
                copy_item[1] = os.path.join(path, filename)

        return copy_list

    @staticmethod
    def execute_copy_list(copy_list):

        # Loop over copy list
        for copy_item in copy_list:

            # define paths
            source = copy_item[0]
            dest = copy_item[1]

            try:
                # If destination item does not exist copy it
                if not os.path.exists(dest):
                    shutil.copy(src=source, dst=dest)
            except EnvironmentError:
                print('Error in shutil.copy for ' + dest)
            else:
                print('OK for ' + dest)

    #################################
    #
    # Abstract base properties/methods
    #
    #################################

    @property
    @abstractmethod
    def mushaf_group_name(self) -> str:
        """
        the name of the mushaf group (e.g. KingFahad, urdu15, warsh)
        """
        pass

    @property
    @abstractmethod
    def image_base_folder(self) -> str:
        """
        Base folder where to find image files
        """
        pass

    @property
    @abstractmethod
    def image_groups(self) -> list:
        """
        List of image groups
        """
        pass

    @property
    @abstractmethod
    def image_group_offset(self):
        """
        Offset to add on image group
        """
        pass

    @abstractmethod
    def get_image_file_name(self, image_number) -> str:
        """
        Method implemented for each image folder to get the image file name

        :param image_number:
        """
        pass
