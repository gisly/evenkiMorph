#encoding=utf-8
__author__ = 'gisly'
import codecs
import os
from evenkiMorphProcessor import EvenkiMorphProcessor
import ConfigParser


import unittest
class TestSequenceFunctions(unittest.TestCase):
    RES_DELIM='\n'
    WORD_DELIM='\t'
    
    HEAD_NUM = 0
    ANALYSIS_NUM = 1
    
    TEST_FOLDER=None
    TEST_MARKER='_mine'
    TEXT_EXT='.txt'
    
    config = ConfigParser.RawConfigParser()
    CONFIG_NAME = 'settings.ini'
    
    config.read(os.path.join(os.path.dirname(__file__), CONFIG_NAME))
    TEST_FOLDER = config.get('tests', 'test_folder')

        
    
    

    def processFile(self, origfile, testFile):
        print('=========='+testFile+'==========')
        programResList=EvenkiMorphProcessor().processFile(origfile).decode('utf-8').split(self.RES_DELIM)
        with codecs.open(testFile, 'r', 'utf-8') as testResFin:
            testRes = self.processListOfLines(testResFin)
            programRes = self.processListOfLines(programResList)
            assert(testRes==programRes)

                
    def processListOfLines(self, listOfLines):
        res=[]
        testLineHeadWordPrev = None
        wordList = []
        for line in listOfLines:
            testLineStripped, testLineParts = self.getLineWordParts(line)
            if self.isEmptyLine(testLineParts):
                continue
            testLineHeadWord = self.getHeadWord(testLineParts)
            if testLineHeadWordPrev is None or testLineHeadWord!= testLineHeadWordPrev:
                res.append(sorted(wordList))
                wordList = [testLineStripped]
                testLineHeadWordPrev = testLineHeadWord
            else:
                wordList.append(testLineStripped)
        res.append(sorted(wordList))      
        return res
    
    def getLineWordParts(self, line):
        testLineStripped=line.strip()
        return  [testLineStripped, self.getWordParts(testLineStripped)]

    def testProcessFolder(self):
        for filename in os.listdir(self.TEST_FOLDER):
            if self.TEST_MARKER in filename:
                testFile=os.path.join(self.TEST_FOLDER, filename)
                origfile=os.path.join(self.TEST_FOLDER, filename.split(self.TEST_MARKER)[0]+self.TEXT_EXT)
                self.processFile(origfile, testFile)


    def getWordParts(self, wordLine):
        return wordLine.split(self.WORD_DELIM)
    
    def getHeadWord(self, lineParts):
        return lineParts[self.HEAD_NUM]
    
    def getAnalysisNum(self, lineParts):
        return lineParts[self.ANALYSIS_NUM]
    
    def isEmptyLine(self, lineParts):
        return len(lineParts)<2

