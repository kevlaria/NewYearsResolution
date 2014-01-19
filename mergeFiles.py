import os
import filePaths as fp

input_directory_name = 'data_raw'
output_file_name = 'New Years Resolution_merged.tsv'
output_directory_name = 'merged'

def main():
    """
    Merge files of the format "New Years Resolution_####.tsv" 
    in the data_raw directory and outputs into the "merged" directory
    """
    output_path = fp.set_output_file_path(output_file_name, output_directory_name) 
    output = open(output_path, 'a')
    for h1 in range(3):
        for h2 in range(10):
            for m1 in range(6):
                for m2 in range(10):
                    file_name = 'New Years Resolution_' + str(h1) + str(h2) + str(m1) + str(m2) + '.tsv'
                    file_path = fp.get_file_path(file_name, input_directory_name)
                    if fp.filename_exists(file_path):
                        file = open(file_path, 'r')
                        file.next()
                        for line in file:
                            output.write(line)
                        file.close()
    output.close()



if __name__ == "__main__":
    main()
