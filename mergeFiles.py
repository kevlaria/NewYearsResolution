import os
import sys
import filePaths as fp


def main(argv):
    """
    Merge files of the format <search_term>_####.tsv" 
    in the data_raw directory and outputs into the "merged" directory
    """

    

    if validate_argv(argv) is False:
        print "Usage: mergeFiles.py <search_term>"
        sys.exit()

    input_directory_name = 'data_raw'
    search_term = argv[0]
    output_file_name = search_term + '_merged.tsv'
    output_directory_name = 'merged'


    output_path = fp.set_output_file_path(output_file_name, output_directory_name) 
    output = open(output_path, 'a')
    for h1 in range(3):
        for h2 in range(10):
            for m1 in range(6):
                for m2 in range(10):
                    file_name = search_term + '_' + str(h1) + str(h2) + str(m1) + str(m2) + '.tsv'
                    file_path = fp.get_file_path(file_name, input_directory_name)
                    if fp.filename_exists(file_path):
                        file = open(file_path, 'r')
                        file.next()
                        for line in file:
                            output.write(line)
                        file.close()
    output.close()

def validate_argv(argv):
    """
    List[String,...] -> Boolean
    Takes a command line argument and ensures that only one argument is input
    """
    if len(argv) != 1:
        return False
    return True

if __name__ == "__main__":
    main(sys.argv[1:])
