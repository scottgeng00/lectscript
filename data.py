import os
import re
import json
import datetime

### takes in srt file name and returns a raw array of the data 
### THIS FUNCTION IS NOT GUARENTEED TO WORK LOL

def load_data_srt(file_name):
    #file_path = os.path.join('..', "subtitles", "srt", file_name)
    #print(file_path)

    #get data into array

    element = {"LINE": 1, "TIME": 2, "TEXT": 3, "SPACE": 0}
    data = []

    with open(file_name, 'r') as f:
        #structure of the file is LINE, TIME, TEXT, SPACE
        count = 0
        block = [] 
        for line in f:
            count += 1
            if (count % 4 == element["SPACE"]):
                data.append(block)
                block = []
            else:
                block.append(line)
    return data

def load_data_json(file_name):
    #file_path = os.path.join('..', "subtitles", "json", file_name)
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

### takes in raw array data and cleans up the data inside the array before returning it (inplace)

def clean_data_srt(data):
    for entry in data:
        entry[0] = int(entry[0].strip())        #clean line number and convert to int

        #00:02:07,744
        times = entry[1].strip().split(" --> ")             #clean timestamp and store as duple of datetime
        time1 = datetime.datetime.strptime(times[0], '%H:%M:%S,%f').time()
        time2 = datetime.datetime.strptime(times[1], '%H:%M:%S,%f').time()
        entry[1] = (time1, time2)
    return data


def clean_data_json(rawdata):
    data = []
    counter = 1
    for entry in rawdata:
        clean = []
        clean.append(counter)
        clean.append((entry['start'], entry['end']))
        clean.append(entry['content'] + '\n')
        counter += 1
        data.append(clean)
    return data


### take in clean array and return one string containing transcript. If doprint parameter is True, also prints the transcript with line nums 

def get_text(data, doprint: bool):
    textstr = ""
    for entry in data:
        if(doprint):
            print("<" + str(entry[0]) + "> " + entry[2].strip())
        textstr = textstr + entry[2]
    return textstr


### take in a string of text with newline charcters and a search string (ie what you would type into the ctrl-f box) 
### and then return an array containing duples of (matched text, line number) in the textstr where the searchstr occurs

def searchall(textstr, searchstr):
    
    searchstr = searchstr.replace(" ", '\s*')
    #print(searchstr)
    pattern = re.compile(searchstr, re.IGNORECASE|re.MULTILINE)

    matches = re.finditer(pattern, textstr)
    matcharr = []
    for match in matches:
        matchline = textstr.count('\n', 0, match.start()) + 1
        #print("\""+ match.group() + "\"\nfound at line " + str(matchline)) 
        matcharr.append((match.group(), matchline))
    return matcharr


def json_to_srt(data):

    srtdata = []
    for entry in data:
        srtentry = []
        srtentry.append(entry[0])
        start_t = datetime.timedelta(seconds=entry[1][0]) 
        end_t = datetime.timedelta(seconds=entry[1][1]) 
        srtentry.append((start_t, end_t))
        srtentry.append(entry[2])
        srtdata.append(srtentry)
    return srtdata