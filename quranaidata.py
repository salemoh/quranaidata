from imagefiles import ImageFiles
from mushafs import kingfahad, urdu15, warsh

######################
#
# Main file
#
######################

if __name__ == '__main__':
    ImageFiles.set_output_path(output_folder=r'C:\objdetect\data',
                               out_suffixes=['train', 'validate', 'test'])

    kingfahad = kingfahad.KingFahad()
    urdu15 = urdu15.Urdu15()
    warsh = warsh.Warsh()

    ImageFiles.add_mushaf(kingfahad)
    ImageFiles.add_mushaf(urdu15)
    ImageFiles.add_mushaf(warsh)

    # Generate copy list that shuffled
    validate_list = ImageFiles.all_copy_list('validate', count=30)

    print(validate_list)
    print(ImageFiles.stats)

    ImageFiles.execute_copy_list(validate_list)
