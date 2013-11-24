# coding=utf-8
__author__ = 'gisly'
import codecs
import subprocess
import sys, os
from cyrillicToLatin import cyrToIPA
import ConfigParser
import socket


class EvenkiMorphProcessor(object):   
    ####character constants
    FLOOKUP_FILENAME = None
    EVENKI_COMPILED_FILENAME = None
    UDP_IP = "127.0.0.1"
    UDP_PORT = 6062
    

    LINE_DELIM='\r\n'
    
    config = ConfigParser.RawConfigParser()
    CONFIG_NAME = 'settings.ini'


    def __init__(self):
        self.config.read(os.path.join(os.path.dirname(__file__), self.CONFIG_NAME))
        self.FLOOKUP_FILENAME = self.config.get('foma', 'flookup')
        self.EVENKI_COMPILED_FILENAME = self.config.get('foma', 'evenki_compiled')
        self.UDP_IP = self.config.get('UDP', 'UDP_IP')
        self.UDP_PORT = self.config.getint('UDP', 'UDP_PORT')
        
        print self.UDP_IP
        print self.UDP_PORT


    def processFileWriteResult(self, filename):
        res=self.callProcessor(filename)
        self.writeTextToFile(res.decode('utf-8'),filename+'_res.txt')

    def processFile(self, filename):
        return self.callProcessor(filename)

    def callProcessor(self, newFileName):
        '''calls foma on the file and grabs the output stream'''
        [stdout,stderr]=subprocess.Popen("type "+newFileName+
                                "|"+self.FLOOKUP_FILENAME+" "+ self.EVENKI_COMPILED_FILENAME,
            stdout=subprocess.PIPE, shell=True).communicate()
        if stderr:
            raise Exception(stderr)
        return stdout
    
    def callProcessorText(self, text):
        res = dict()
        for word in text:
            if len(word)>0:
                [stdout,stderr]=subprocess.Popen("echo "+word+
                                        "|"+self.FLOOKUP_FILENAME+" "+ self.EVENKI_COMPILED_FILENAME,
                    stdout=subprocess.PIPE, shell=True).communicate()
                if stderr:
                    raise Exception(stderr)
                res[word]=stdout
        return res
    
    
    def callProcessorUDP(self, text):
        sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        res = dict()
        for word in text:
            if len(word)>0:
                sock.sendto(word, (self.UDP_IP, self.UDP_PORT))
                analysis = ''
                while True:
                    analysis, addr = sock.recvfrom(7000) # buffer size is 1024 bytes
                    break
                res[word]=analysis
        return res

    def getNormalizedFile(self, filename):
        text=self.getTextFromFile(filename)
        text=self.normalizeText(text)
        newFileName=filename+'_prepared.txt'
        self.writeTextToFile(text, newFileName)
        return newFileName

    def getTextFromFile(self, filename):
        with codecs.open(filename, 'r', 'utf-8') as fin:
            return fin.read()

    def normalizeText(self, text):
        '''converts the text from cyrillic to ASCII-based fonetic code
        and formats it the way foma requires'''
        text=cyrToIPA(text)
        return self.tokenize(text)

    def writeTextToFile(self, text, newFileName):
        with codecs.open(newFileName, 'w', 'utf-8') as fout:
            fout.write(text)

    def tokenize(self, text):
        return text.replace(' ',self.LINE_DELIM).replace('-',self.LINE_DELIM)

def main():
    if len(sys.argv)<2:
        print('usage: evenkiMorphProcessor.py <filename>')
    else:
        processor=EvenkiMorphProcessor()
        normalizedFile=processor.getNormalizedFile(sys.argv[1])
        
        processor.processFileWriteResult(normalizedFile)

if __name__ == "__main__":
    main()
"""processor=EvenkiMorphProcessor()
normalizedFile=processor.getNormalizedFile("D:\\SibLang\\Evenki\\evenkiTexts\\tests\\evenkiTests\\20120308_kodakchon_novowels.txt")
        
processor.processFileWriteResult(normalizedFile)"""


