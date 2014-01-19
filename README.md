NewYearsResolution
==================

Objective of this project is to:

a) Experiment with Twitter API
b) Using harvested tweets, randomly generate new New Years Resolution-related tweets based on the vocabulary available in the harvested tweets

- twitterTwitterStream.py 

Usage: twitterTwitterStream.py <search term> <minute>
Extracts up to 3000 tweets using <search term>, at every hour on <minute>
(Update: this no longer works as Twitter now requires SSH when accessing the API)

Harvested tweets are placed in the /data_raw directory. One file is generated per hour, in the format <search term>_HHMM.tsv , where HHMM is the starting hour and minute of the harvesting

- mergeFiles.py

Usage: mergeFiles.py <search_term>
Merges all the files in the /data_raw directory, and stores the resulting data in the /merged directory

- tokenizeTweets.py

Usage: tokenizeTweets.py <file name> <file directory> <n (for n gram)>
1. Creates n-grams for a file containing tweets
2. Creates a list of tokens from the same file

This module will only include tweets that contain the terms "is to" or ":", and only includes the words following these two words. Phrases following these terms tend to provide the 'meat' of a Tweeter's resolution (eg "My New Years Resolution is to lose weight" etc).

ngrams are in the form: <word 1>: "<word 1> <word 2>, <word 1> <word 3>, <word 1> <word 3>" etc. Repeated ngrams are not filtered out.

ngrams are stored in the /ngrams folder
tokens are stored in the /tokens folder

- createTweets.py

Usage: tokenizeTweets.py <file name> <file directory> <start term>
Randomly generates a tweet of length 10 words, starting with <start term>
The tweet is generated thus:
- Using the start term, look up all ngrams that start with this keyword.
- From the list of ngrams, randomly select one, and return the second word in that list
- This second word then becomes the keyword for the next word

The process stops when either a) The next word is a '$', an end marker for the original tweet, or b) 10 words

- markovCreateTweets.py

Usage: tokenizeTweets.py <file name> <file directory>
To provide a comparison to createTweets.py, I located code that generates text using a trigram Markov chain
Uses a trigram Markov chain (found on https://gist.github.com/agiliq/131679), randomly generate sentences from token list
