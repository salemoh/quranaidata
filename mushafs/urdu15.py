from quranaidata import ImageFiles


class Urdu15(ImageFiles):
    """
        Contains the groups for Urdu mushaf
    """

    @property
    def mushaf_group_name(self): return 'urdu15'

    @property
    def image_base_folder(self): return r'C:\Users\moham\Source\Repos\GoldenQuranRes\images\urdu15'

    @property
    def image_groups(self):
        return [
            [3, 208],
            [209, 404],
            [405, 518],
            [519, 587],
            [588, 602],
            [603, 611]
        ]

    @property
    def image_group_offset(self): return 1

    def get_image_file_name(self, image_number):
        """
        Method used to return the image file name from
        an image number in image_groups

        :type image_number: int
        """
        return str(image_number).zfill(3) + '.png'
