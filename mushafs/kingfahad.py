from quranaidata import ImageFiles


class KingFahad(ImageFiles):
    """
        Contains the groups for King Fahad mushaf
    """

    @property
    def mushaf_group_name(self): return 'KingFahad'

    @property
    def image_base_folder(self): return r'C:\Users\moham\Source\Repos\GoldenQuranRes\images\kingFahad'

    @property
    def image_groups(self):
        return [
            [1, 207],
            [208, 404],
            [405, 517],
            [518, 581],
            [582, 595],
            [596, 604]
        ]

    @property
    def image_group_offset(self): return 0

    def get_image_file_name(self, image_number):
        """
        Method used to return the image file name from
        an image number in image_groups

        :type image_number: int
        """
        return 'page' + str(image_number).zfill(3) + '.png'
