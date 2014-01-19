import os
import sys

def get_file_path(input_file, input_directory_name):
    """
    String, String -> String
    Constructs a directory path for opening an input file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, input_directory_name)
    path = os.path.join(dest_dir, input_file)
    return path

def set_output_file_path(output_file, output_directory_name):
    """
    String -> String
    Constructs a directory path for opening an output file
    """
    mkdir(output_directory_name)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, output_directory_name)
    path = os.path.join(dest_dir, output_file)
    return path


def mkdir(directory_name):
    """
    Makes a directory. Exception is caught in this function.
    """
    try:
        os.mkdir(directory_name)
    except OSError:
        pass

def filename_exists(filename):
    """
    String -> Boolean
    Given a file path, tries to open the file. Returns true if the file can be opened.
    """
    try:
        f = open(filename, 'r')
        f.close()
        return True
    except:
        return False
