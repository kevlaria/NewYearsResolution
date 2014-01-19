"""
Utility module for creating dictionaries and ngrams
"""

def create_ngrams(tokens_list, n):
    """
    List[String,...], int ->  List[String, ...]
    Takes in a list of tokens, and 'n' (2 = bigram, 3 = trigram etc) and create a list of ngram strings
    """
    ngram_list = []
    for tokens in tokens_list:
        for i in range(len(tokens)):
            if i + (n - 1) < len(tokens):
                word_list_string = tokens[i]
                for j in range(n - 1):
                    word_list_string = word_list_string + ' ' + tokens[(i + j + 1)]
                ngram_list.append(word_list_string)
    return ngram_list


def create_ngram_dict(ngrams):
    """
    List[String, ...] -> Dict{String: [[String,...]]}
    Given a list of ngrams, create a dictionary where the key is the first word of the ngram and the value is the ngram
    """
    ngram_dictionary = dict()
    for ngram in ngrams:
        words = ngram.split()
        key = words[0]
        if key not in ngram_dictionary:
            ngram_dictionary[key] = [ngram]
        else:
            ngram_dictionary[key].append(ngram)
    return ngram_dictionary