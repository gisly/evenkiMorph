#encoding=utf-8
import re
from flask import jsonify

import socket

from cyrillicToLatin import cyrToIPA
import evenkiMorphProcessor

__author__ = 'gisly'
from flask import Flask, request, render_template



RES_DELIM='\n'
RES_WORD_DELIM = '\t'
LINE_DELIM='\r\n'

UNKNOWN='?'





app = Flask(__name__)
app.config.from_object(__name__)
evenkiMorphProcessor = evenkiMorphProcessor.EvenkiMorphProcessor()



@app.route('/')
def evenki_test_parser():
    return render_template('evenki_test_parser.html')


@app.route('/parse_text')
def parse_text():
    text = request.args.get('evenki_text')
    tokenizedText = tokenize(text)
    latCyr, tokenizedLatin = cyrToLatin(tokenizedText)
    
    
    #morphRes = evenkiMorphProcessor.callProcessorText(tokenizedLatin)
    
    try:
        morphRes = evenkiMorphProcessor.callProcessorUDP(tokenizedLatin)
    except Exception, e:
        return jsonify(error='Sorry, an error occurred. Try again later')
    
    res=dict()
    for word, analysis in morphRes.items():
        analysisRes = analysis.strip().decode('utf-8').split(RES_DELIM)
        
        if not isUnknown(analysisRes):
            analysisRes = [resPart.split(word, 1)[1] for resPart in analysisRes]
            res[latCyr[word]]=analysisRes
    return jsonify(result=res)


def tokenize(text):
    return re.split(ur'\?|!|,|-|\.|\s|:|;|\\[|\\]', text.strip())

def isUnknown(res):
    return UNKNOWN in res[0]

def cyrToLatin(tokenizedText):
    latCyr = dict()
    latRes = []
    for word in tokenizedText:
        word = word.strip()
        latWord = cyrToIPA(word)
        latCyr[latWord]=word
        latRes.append(latWord)
    return latCyr,latRes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2030)
