from quranaidata import ImageFiles


class Warsh(ImageFiles):
    """
        Contains the groups for Warsh mushaf
    """

    @property
    def mushaf_group_name(self): return 'warsh'

    @property
    def image_base_folder(self): return r'C:\Users\moham\Source\Repos\GoldenQuranRes\images\warsh'

    @property
    def image_groups(self):
        return [
            [4, 179],
            [180, 363],
            [364, 470],
            [471, 534],
            [535, 549],
            [550, 559]
        ]

    @property
    def image_group_offset(self): return 3

    def get_image_file_name(self, image_number):
        """
        Method used to return the image file name from
        an image number in image_groups

        :type image_number: int
        """
        return str(image_number).zfill(4) + '.png'
