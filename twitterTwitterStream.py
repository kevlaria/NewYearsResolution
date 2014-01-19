import twitterConnect as tc
import csv
from datetime import datetime
from time import sleep
import sys
import os

def main(argv):
    """
    Given a topic and a start time, extracts 2000 tweets from a TwitterStreamonce an hour, and stores in a TSV file 
    """
    if validate_argv(argv) is False:
        print "Usage: twitterTwitterStream.py <search term> <minute>"
        sys.exit()
    directory_name = 'data_raw'
    mkdir(directory_name)
    while True:
        topic = argv[0]
        minute_start = argv[1].strip()
        minute = datetime.now().strftime('%M')
        if minute == minute_start:
            twitter_stream = tc.get_twitter_stream()
            start_time = datetime.now()
            output_file = create_output_file_name(topic, directory_name)
            try:
                output = open(output_file, 'w')
            except IOError:
                print "File error...exiting"
                sys.exit()
            csv_writer = csv.writer(output, delimiter='\t')
            csv_writer.writerow(['id', 'text', 'location', 'time_zone', 'date'])
            stream = twitter_stream.statuses.filter(track=topic)
            try:
                write_tweets(csv_writer, output, stream, start_time)
            except:
                print "Exception raised from writing tweets. Exiting..."
                sys.exit()
        else:
            sleep(45)

def create_output_file_name(topic, directory_name):
    """
    String, String -> String
    Creates a name for the output file.
    Returns a string form of the file name with the relevant path
    """
    time_str = datetime.now().strftime('%H%M')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, directory_name)
    output_file = topic + '_' + time_str + '.tsv'
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

def validate_argv(argv):
    """
    List[String,...] -> Boolean
    Takes a command line argument and ensures that a) there are only two arguments and b) 2nd argument is in the form 'XY', where 'X' is a digit from 0 - 5 and 'Y' is a digit from 0 - 9. Returns False if either test fails.
    """
    if len(argv) != 2:
        return False
    if validate_minute_input(argv[1]) is False:
        return False
    return True

def validate_minute_input(input):
    """
    Integer -> Boolean
    Takes a string of length 1 and returns True if it's 0, 1, 2, 3, 4, or 5
    """
    if is_int(input):
        if len(input) == 2:
            if int(input[0]) in [0, 1, 2, 3, 4, 5]:
                return True
    return False
        

def is_int(input):
    """
    Unknown -> Boolean
    Returns True only if the input is a digit
    """
    try:
        int(input)
        return True
    except:
        return False

def write_tweets(csv_writer, output, stream, start_time):
    """
    Stores extracted tweets in an output file in TSV format. Process is completed the earlier of 30 minutes or 2000 tweets.
    """
    count = 0
    for item in stream:
        tweets = []
        tweets.append(item)
        for tweet in tweets:
            current_time = datetime.now()
            time_diff = current_time - start_time
            if time_diff.total_seconds() > (30 * 60):
                output.close()
                stream.close()
                print "Closing after 30 minutes"
                return
            if count < 2000:
                text = tweet['text'].encode('utf-8').strip()
                time_zone = tweet['user']['time_zone']
                if 'RT' not in text and 'http' not in text and tweet['lang'] == 'en':
                    fields = []
                    fields.append(tweet['id_str'].encode('utf-8').strip())
                    fields.append(text)
                    fields.append(tweet['user']['location'].encode('utf-8').strip())
                    fields.append(time_zone)
                    fields.append(tweet['created_at'].encode('utf-8').strip())
                    print fields
                    csv_writer.writerow(fields)
                    count = count + 1
            else:
                output.close()
                stream.close()
                print "Done!"
                return
    
 
if __name__ == "__main__":
    main(sys.argv[1:])

