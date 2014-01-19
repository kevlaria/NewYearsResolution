import filePaths as fp
import sys
import json
import random

def main(argv):
    """
    Creates a randomly generated tweet based on a single initial keyword. Example: createTweets.py New\ Years\ Resolution_ngram_3.json ngrams stop
    """
    if validate_argv(argv) is False:
        print "Usage: tokenizeTweets.py <file name> <file directory> <start term>"
        sys.exit()
    file_name = argv[0]
    input_directory_name = argv[1]
    search_term = argv[2].lower()
    input_path = fp.get_file_path(file_name, input_directory_name)
    ngram_dictionary = extract_dictionary(input_path)
    if validate_search_term(search_term, ngram_dictionary) is False:
        print "'" + search_term + "' does not exist in tweet dictionary" 
        sys.exit()
    sentence_list = create_sentence(search_term, ngram_dictionary)
    count = 0
    while len(sentence_list) < 6 and count < 5: # 5 attempts to create a sentence longer than 6 words (including '$')
        sentence_list = create_sentence(search_term, ngram_dictionary)
        count = count + 1
    if '$' in sentence_list:
        sentence_list.remove('$')
    sentence = ' '.join(sentence_list)
    print sentence


def create_sentence(search_term, ngram_dictionary):
    """
    String, dict{List[String,...]} -> List[String,...]
    Given a search term and an ngram_dictionary, randomly generate a sentence that's not longer than 10 words
    """
    sentence_list = [search_term]
    word = extract_words(search_term, ngram_dictionary, sentence_list)
    count = 0
    sentence_list.append(word)
    while word != "$" and count < 10:
        if validate_search_term(word, ngram_dictionary) is False:
            return sentence_list
        word = extract_words(word, ngram_dictionary, sentence_list)
        if word not in sentence_list:
            sentence_list.append(word)
            count = count + 1
    return sentence_list


def extract_words(search_term, ngram_dictionary, sentence_list):
    """
    String, dict{List[String,...]}}, list[String,...]
    Given a search term and an ngram dictionary, return the next word. Next word is selected based on the most frequent ngram starting with search_term. If there are multiple entries for the most frequent ngram, a random second word from that list of entries is returned
    """

    ngram_list = ngram_dictionary.get(search_term)
    random.shuffle(ngram_list)
    for i in range(len(ngram_list)):
        random_index = random.randint(0, len(ngram_list) - 1)
        ngram = ngram_list[random_index]
        words = ngram.split()
        next_word = words[1]
        i = i + 1
        if (next_word in sentence_list) is False:
            return next_word
    next_word = '$' # Unable to find a word that doesn't already exist in the sentence list, so returning $, the end-of-line symbol
    return next_word
    

def extract_dictionary(file_path):
    """
    String -> dict(string: List[String,...])
    Extracts a dictionary of ngrams from a TSV file
    """
    try:
        input = open(file_path, 'r')
    except:
        print "File not found"
        sys.exit()
    dictionary = json.load(input)
    input.close()
    if validate_input_file(dictionary) is False:
        print "Input file format invalid"
        sys.exit()
    return dictionary
    

def validate_argv(argv):
    """
    List[String,...] -> Boolean
    Takes a command line argument and ensures that a) there are only 3 arguments and b) 1st & 2nd argument is a valid path and file.  False if any of the above are not true
    """
    if len(argv) != 3:
        return False
    file_name = argv[0]
    input_directory_name = argv[1]
    n = argv[2]
    file_path = fp.get_file_path(file_name, input_directory_name)
    if fp.filename_exists(file_path) is False:
        print "File doesn't exist"
        return False
    return True


def validate_input_file(dictionary):
    """
    Dict{String: List[String,...]} -> Boolean
    Determines whether the input file is in the valid format for processing
    """
    if type(dictionary) == dict:
        for key in dictionary:
            if type(key) == unicode:
                if type(dictionary.get(key)) == list:
                    if type(dictionary.get(key)[0]) == unicode:
                        return True
    return False

def validate_search_term(search_term, ngram_dictionary):
    """
    String, dict{dict{int: List[String,...]}} -> Boolean
    Returns true if a search term appears as a key in the ngram_dictionary.
    """
    if search_term in ngram_dictionary:
        return True
    return False


if __name__ == "__main__":
    main(sys.argv[1:])
