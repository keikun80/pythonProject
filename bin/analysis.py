import os , sys
import pickle
from urllib.parse import urlparse, urlencode, quote, unquote
import knusl
import json
import threading
import pandas as pd
import numpy as np
DATADIR = 'DATA'
SEPARATOR = '/'
class KnuSL():

    def data_list(wordname):
        with open('SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
            data = json.load(f)
        result = ['None', 'None']
        for i in range(0, len(data)):
            if data[i]['word'] == wordname:
                result.pop()
                result.pop()
                result.append(data[i]['word_root'])
                result.append(data[i]['polarity'])

        r_word = result[0]
        s_word = result[1]

        #print('어근 : ' + r_word)
        #print('극성 : ' + s_word)
        if s_word == "None":
            s_word = 0
        else:
            pass
        # return r_word, s_word
        return int(s_word)


ksl = KnuSL
def datafilter(dataSet):
    retData = list()
    for line in dataSet:
        #print(line)
        #for words in line:
          #print(words)
        if "Verb" in line:
            #print(line[0])
            #print(words)
            retData.append(line[0])
        if "Adj" in line:
            # print(line[0])
            retData.append(line[0])
            #print(words)
    return retData


def readfiles(ttype):
    retData = []
    dir = DATADIR+SEPARATOR
    fileExt = ttype
    arr = [ os.path.join(dir, file) for file in os.listdir(dir) if file.endswith(fileExt)]
    for fileName in arr:
        t = threading.Thread(target=judgeArticle, args=(fileName, ))
        t.start()
    return retData

def judgeArticle(fileName):
    with open(fileName, 'rb') as f:
        # retData.append(pickle.load(f))
        posWords = datafilter(pickle.load(f))
        pos = 0
        nag = 0
        net = 0
        for word in posWords:
            s_word = ksl.data_list(word)
            if (s_word > 0):
                pos = pos + s_word
            elif (s_word < 0):
                nag = nag + s_word
            else:
                net = net + 1
        print(f'{unquote(fileName[5:-4])}, {pos},{nag}, {net}')



if __name__ == "__main__":
    readfiles("pos")
