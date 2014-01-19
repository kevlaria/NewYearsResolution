import sys
import filePaths as fp
import markov


def main(argv):
    """
    Uses a trigram Markov chain (found on https://gist.github.com/agiliq/131679), randomly generate sentences from token list
    """

    if validate_argv(argv) is False:
        print "Usage: tokenizeTweets.py <file name> <file directory> <start term>"
        sys.exit()
    file_name = argv[0]
    input_directory_name = argv[1]
    path = fp.get_file_path(file_name, input_directory_name)
    input = open(path, 'r')
    text_markov = markov.Markov(input)
    input.close()
    print text_markov.generate_markov_text()


def validate_argv(argv):
    """
    List[String,...] -> Boolean
    Takes a command line argument and ensures that a) there are only 2 arguments and b) 1st & 2nd argument is a valid path and file.  False if any of the above are not true
    """
    if len(argv) != 2:
        return False
    file_name = argv[0]
    input_directory_name = argv[1]
    file_path = fp.get_file_path(file_name, input_directory_name)
    if fp.filename_exists(file_path) is False:
        print "File doesn't exist"
        return False
    return True


if __name__ == "__main__":
    main(sys.argv[1:])
