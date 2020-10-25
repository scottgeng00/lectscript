#! /usr/bin/python3

import nlp
import os
import subprocess
import glob
import argparse
import hashlib
import data as d
import sys
import datetime
import time
from summa import keywords
from summa import summarizer

def main(args):

    TASK_COUNT = 200

    password = args.password
    cleanfiles = not args.keep
    cleancache = args.ignore_cache
    url = args.url

    file_hash = int(hashlib.sha1(url.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
    file_hash = str(file_hash)

    ## make directories if they dont exist

    if not os.path.isdir('./output'):
        os.mkdir('./output')
    if not os.path.isdir('./data'):
        os.mkdir('./data')
    if not os.path.isdir('./data/transcripts'): 
        os.mkdir('./transcripts')
    
    if(cleancache or (len(glob.glob('./data/transcripts/' + file_hash + '.json')) == 0)):
        if password is not None:
            subprocess.run(["zoomdl", "-u", url, "-p", password, "-f",  "./data/" + file_hash], check=True)
        else:
            subprocess.run(["zoomdl", "-u", url, "-f", "./data/" + file_hash], check=True)

        media_file = glob.glob('./data/' + file_hash + '.*')[0]
        subprocess.run(["autosub", media_file, "-C", str(TASK_COUNT), "-o", "./data/transcripts/" + file_hash + '.json', '-F', 'json'], check=True)

    else:
        print("Previously generated transcript found: using cached transcript for this lecture")

    file_name = glob.glob('./data/transcripts/' + file_hash + '.json')[0]

    rawdata = d.load_data_json(file_name)
    data = d.clean_data_json(rawdata)
    textstr = d.get_text(data, False)

    #words = keywords.keywords(textstr, words=10)
    #words = words.split("\n")

    summary = summarizer.summarize(textstr, words=100)
    moments = nlp.get_moments(summary, data, textstr, MIN_SPACE=args.time_space, MAX_COUNT=args.max_moments)
    doc_list = nlp.get_key_phrases(textstr)


    temp = sys.stdout
    sys.stdout = open(args.output, 'w')

    if(args.bookmark is not None):

        try:
            bcsv = open(args.bookmark, 'r')
            print("################# PERSONAL BOOKMARKS #################")
            bcsv.readline(); bcsv.readline(); bcsv.readline()
            for line in bcsv:
                line = line.split(', ')
                timestamp = line[0].split('.')[0]
                print("<" + str(timestamp) + "> " + line[1])
            print()

        except:
            raise FileNotFoundError('The bookmark file you entered doesn\'t exist :(')
            
    print("################# KEY LECTURE CONCEPTS #################")
    for phrase in doc_list[:20]:
        print(phrase.text.strip())

    print("\n\n################# SUGGESTED MOMENTS #################")
    for moment in moments:
        print("<" + moment[0] + ">")
        print(moment[1])
        print()

    print("\n################# LECTURE TRANSCRIPT #################")
    for line in data:
        print("<" + str(datetime.timedelta(seconds=int(line[1][0])))  + "> " + line[2].strip())

    sys.stdout.close()
    sys.stdout = temp
    print("\n##### KEY LECTURE CONCEPTS #####")
    for phrase in doc_list[:20]:
        print(phrase.text.strip())

    print("\n\n##### SUGGESTED MOMENTS #####")
    for moment in moments:
        print(moment[0])
        print(moment[1])
        print()

    if(args.verbose):
        for line in data:
            print("<" + str(line[0]) + "> " + line[2].strip())

    if(args.subtitle is not None):
        srtdata = d.json_to_srt(data)

        sys.stdout = open(args.subtitle, 'w')
        
        for entry in srtdata:
            print(entry[0])

            start_t = entry[1][0]
            end_t = entry[1][1]
            start_str = str(time.strftime('%H:%M:%S', time.gmtime(start_t.seconds))) + ',' + str(int(start_t.microseconds / 1000))
            end_str = str(time.strftime('%H:%M:%S', time.gmtime(end_t.seconds))) + ',' + str(int(end_t.microseconds / 1000))

            print(start_str + ' --> ' + end_str)
            print(entry[2])

        sys.stdout.close()

    if cleanfiles:
        for tmpfile in glob.glob('./data/*.*'):
            subprocess.run(["rm", "-r", tmpfile])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Automatically generate lecture transcripts with key concepts and moments identified.')

    parser.add_argument("url", help="URL of Zoom recording (required)")
    parser.add_argument("-o", "--output", help="Specify output file (default is 'lecture_transcript.txt' in output directory)",
                        type=str, default="output/lecture_transcript.txt")
    parser.add_argument("-p", "--password", help="Password of the video",
                        type=str)
    parser.add_argument("-b", "--bookmark", help="Your bookmark file for the given lecture",
                        type=str)
    parser.add_argument("-v", "--verbose", help="Increase stdout verbosity",
                        action="store_true")
    parser.add_argument("-k", "--keep", help="Keep downloaded lectures",
                        action="store_true")
    parser.add_argument("-s", "--subtitle", help="Generate subtitle file in srt format",
                        type=str)
    parser.add_argument("-i", "--ignore-cache", help="Ignore cached data and recreate everything",
                        action="store_true")
    parser.add_argument("-m", "--max-moments", help="Max important moments to return (default 5)", default=5, type=int)
    parser.add_argument("-t", "--time-space", help="Min time (s) between important moments (default 600)", default=600, type=int)

    args = parser.parse_args()
    #print(args)
    main(args)