import csv
import sys
import nltk as nltk
import re
import json
import dictionaryGenerator as dg
import filePaths as fp
import copy

def main(argv):
    """
    Creates n-grams from the file New Years Resolution_merged.tsv. Output in JSON format
    """
    if validate_argv(argv) is False:
        print "Usage: tokenizeTweets.py <file name> <file directory> <n (for n gram)>"
        sys.exit()
    file_name = argv[0]
    input_directory_name = argv[1]
    n_for_ngrams = int(argv[2])
    input_path = fp.get_file_path(file_name, input_directory_name)
    tweets = extract_tweets(input_path)
    tweets_deduped = dedupe_and_tokenize(tweets)

    # for creating an ngram dictionary 

    ngrams = dg.create_ngrams(tweets_deduped, n_for_ngrams)
    ngram_dict = dg.create_ngram_dict(ngrams)
    output_path = fp.set_output_file_path('New Years Resolution_ngram_' + str(n_for_ngrams) + '.json', 'ngrams')
    output_ngram(ngram_dict, output_path)

    # for creating a list of tokens. Removing the words "New Years Resolution" as well.

    tokens = break_down_sentences(tweets_deduped)
    tokens_cleaned = remove_tokens(tokens, ['new', 'years', 'resolution', ':'])
    output_path2 = fp.set_output_file_path('New Years Resolution_tokens.tsv', 'tokens')
    output_tokens(tokens_cleaned, output_path2)
    

def break_down_sentences(list_of_tokenized_sentences):
    """
    List[List[String,...]] -> List[String,...]
    Given a list of tokenized sentences, create a list of all the tokens
    """
    list_of_tokens = []
    for token in list_of_tokenized_sentences:
        list_of_tokens.extend(token)
    return list_of_tokens

def remove_tokens(tokens, remove_list):
    """
    List[String,...], List[String,...] -> List[String,...]
    Remove specific words from the tokens list
    """
    for word in remove_list:
        while word in tokens:
            tokens.remove(word)
    return tokens

def output_tokens(tokens, output_path):
    """
    List[String,...], String -> File
    Write a dictionary to file
    """
    try:
        f = open(output_path, 'w')
        for token in tokens:
            if token != "$" and token != "^":
                f.write(token + '\n')
        f.close()
    except:
        print "IO error (tokens), exiting"
        sys.exit()


def dedupe_and_tokenize(tweets):
    """
    List[String,...] -> List[List[String,...]]
    Dedupes tweets by id and returns a list of tokenized sentences.
    """
    tweet_dict = {}
    for tweet in tweets:
        id = tweet[0]
        str = tweet[1].lower()
        if id not in tweet_dict:
            tokens = tokenize(str)
            if tokens:
                tweet_dict[id] = tokens
    return tweet_dict.values()


def tokenize(str):
    """
    String -> List[String,...]
    Tokenizes a string.
    """
    pattern = r'''(?x) \w+('\w+)* | @\w+ | : | [#]\w+'''
    tokens = ['^']
    tokens.extend(nltk.regexp_tokenize(str, pattern))
    tokens.append('$')
    tokens_un_hexed = remove_hex(tokens)
    tokens_cleaned = include_only_to_and_colon(tokens_un_hexed)
    if tokens_cleaned:
        return tokens_cleaned

def include_only_to_and_colon(tokens):
    """
    List[String,...] -> List[String,...]
    Filters out all tweets without the words 'to' or ':'. Output excludes either 'to' or ':'
    """
    output = []
    if "is" in tokens:
        index = tokens.index("is")
        if index + 2 < len(tokens):
            if tokens[index + 1] == "to":
                output = copy.copy(tokens[index + 2:])
                return output
    if ":" in tokens:
        index = tokens.index(":")
        if index + 1 < len(tokens):
            output = copy.copy(tokens[index + 1:])
            return output
        

def remove_hex(tokens):
    """
    List[String,...] -> List[String,...]
    Remove all non-ascii tokens (eg '\xf0'), tokens with an '@', and with a '#'
    """
    output = []
    for token in tokens:
        str = token.decode('ascii', 'ignore')
        if str != '' and '@' not in str and '#' not in str:
            output.append(str)
    return output


def extract_tweets(file_path):
    """
    String -> List[String,...]
    Extracts tweets from a TSV file
    """
    try:
        input = open(file_path, 'r')
    except:
        print "File not found"
        sys.exit()
    csv_reader = csv.reader(input, delimiter = '\t')
    tweets = []
    for line in csv_reader:
        tweets.append(line)
    input.close()
    if validate_input_file(tweets) is False:
        print "Input file invalid format"
        sys.exit()
    return tweets


def output_ngram(dictionary, output_path):
    """
    Dict{String, List[int, String)} -> JSON file
    Write a dictionary to file
    """
    try:
        f = open(output_path, 'w')
        json.dump(dictionary, f)
        f.close()
    except:
        print "IO error, exiting"
        sys.exit()


def validate_argv(argv):
    """
    List[String,...] -> Boolean
    Takes a command line argument and ensures that a) there are only 3 arguments and b) 1st & 2nd argument is a valid path and file c) 3rd argument is a positive integer. Returns False if any of the above are not true
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
    try:
        n_int = int(n)
        if n_int < 2 or n_int > 5:
            print "n must be greater than 1 or less than 6"
            return False
    except:
        return False
        print "n must be an integer"
    return True


def validate_input_file(tweets):
    """
    List[String,...] -> Boolean
    Validates that the input file is of the correct format
    """
    if type(tweets) == list:
        for line in tweets:
            if len(line) == 5:
                for item in line:
                    if type(item) == str or type(item) == unicode:
                        return True
    return False 

if __name__ == "__main__":
    main(sys.argv[1:])

