import data as d
import spacy
import pytextrank
import os
import summa
import math
import datetime
from summa import keywords
from summa import summarizer

def get_key_phrases(textstr):
    nlp = spacy.load("en_core_web_sm")
    doc_list = []

    # add PyTextRank to the spaCy pipeline
    tr = pytextrank.TextRank()
    nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    doc = nlp(textstr)

    # examine the top-ranked phrases in the document
    for p in doc._.phrases:
        #print("{}".format(p.text))
        doc_list.append(p)
    return doc_list


def get_moments(summary, data, textstr, MAX_COUNT=5, MIN_SPACE=600):
    moments = []
    last_time = -(math.inf)            #a big negative
    count = 0

    summary = summary.split("\n")
    for sentence in summary:
        if(count >= MAX_COUNT):
            break
        matches = d.searchall(textstr, sentence)
        line = matches[0][1]
        if((last_time + MIN_SPACE) <= data[line-2][1][0]):
            last_time = data[line-2][1][0]
            preview = ""
            preview += data[line-2][2]
            preview += data[line-1][2]
            preview += data[line][2].strip()

            timestamp = datetime.timedelta(seconds=int(data[line-2][1][0]))

            #print(str(timestamp))
            #print(preview)
            moment = [str(timestamp), preview, line]
            moments.append(moment)
            count += 1
        else:
            pass
    return moments


