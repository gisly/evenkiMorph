# coding=utf-8
__author__ = 'gisly'

import xml.etree.ElementTree as ET


EAF_DELIMITER = '_'
TECHNICAL_DELIMITER = '#'

GLOSS_XPATH = ".//TIER[@TIER_ID='gl']/ANNOTATION/REF_ANNOTATION"
FON_XPATH = ".//TIER[@TIER_ID='fon']/ANNOTATION/REF_ANNOTATION"
POS_XPATH = ".//TIER[@TIER_ID='pos']/ANNOTATION/REF_ANNOTATION"
FONWORD_XPATH = ".//TIER[@TIER_ID='fonWord']/ANNOTATION/REF_ANNOTATION"
RUS_XPATH = ".//TIER[@TIER_ID='rus']/ANNOTATION/REF_ANNOTATION"
LANGUAGE_XPATH = ".//TIER[@TIER_ID='%s']/ANNOTATION/ALIGNABLE_ANNOTATION"


ANNOTATION_VALUE_XPATH = '/ANNOTATION_VALUE'

ANNOTATION_REF_ATTRIBUTE = 'ANNOTATION_REF'
ANNOTATION_ID_ATTRIBUTE = 'ANNOTATION_ID'

EAF_EXT = '.eaf'

POS_CONVERSION = {u'сущ':'N', u'гл':'V', u'кол.числ':'Card', u'прил':'Adj', u'нареч':'Adv', u'част':u'Part'}

def getLocationByFilename(filename):
    filenameParts = filename.split(EAF_DELIMITER)
    return filenameParts[1].lower()



def getTextInfo(filename, languageCode, isToUseFonInsteadOfFonWord = False, isToGetRus = True, isToIgnoreErrors = False):
    root = getRoot(filename)
    sentences = getSentences(root, languageCode)
    textInfo = []
    for sentence in sentences:
        textInfoSentence = dict()
        textInfoSentence['sentence'] = getAnnotationValueFromElement(sentence)
        
        
        if isToGetRus:
            textInfoSentence['sentenceRus'] = getTranslationBySentence(root, sentence)
        else:
            textInfoSentence['sentenceRus'] = 'unknown'
        
        try:
        
            textInfoSentence['morphology'] = getTokensBySentence(root, sentence, textInfoSentence['sentenceRus'], isToUseFonInsteadOfFonWord)
        except Exception, e:
            if isToIgnoreErrors:
                raise e
            else:
                textInfoSentence['morphology'] = []
                print str(e)
        
        textInfo.append(textInfoSentence)
    return textInfo
        
        
    

def getTokensBySentence(root, sentence, rusSentence, isToUseFonInsteadOfFonWord = False):
    sentenceId = getElementId(sentence)
    fonWords = getFonWordsById(root, sentenceId)
    morphInfos = []
    for fonWord in fonWords:
        morphInfo = dict()
        
        
        
        morphInfo['token'] = getAnnotationValueFromElement(fonWord, rusSentence)
        
        morphInfo['analysis'] = getAnalysis(root, fonWord, morphInfo['token'], rusSentence)
        
        if isToUseFonInsteadOfFonWord:
            fonTotal = ''.join([analysisPart['fon'] for analysisPart in morphInfo['analysis']])
            morphInfo['token'] = fonTotal.replace('-', '').replace('=', '').replace(u'∅', '')
        
        morphInfo['pos'] = getPos(root, fonWord)
        morphInfos.append(morphInfo)
    return morphInfos

def getTranslationBySentence(root, sentence):
    sentenceId = getElementId(sentence)
    
    print RUS_XPATH + "[@" + \
                      ANNOTATION_REF_ATTRIBUTE + \
                      "='" + sentenceId+ "']"
    
    return getAnnotationValueFromElement(root.find(RUS_XPATH + "[@" + 
                      ANNOTATION_REF_ATTRIBUTE +  
                      "='" + sentenceId+ "']"));


def getAnalysis(root, fonWord, fonToken, rusSentence, isToAddFon = False):
    fonWordId = getElementId(fonWord)
    fons = getFonsById(root, fonWordId)
    analysis = []
    if len(fons) == 0:
        raise Exception('No fon elements for fonWord with id %s (%s), sentence: %s' % (fonWordId, fonToken, rusSentence))
    
    for fon in fons:
        fonId = getElementId(fon)
        gloss = getGlossById(root, fonId)
        
        
        fonValue = getAnnotationValueFromElement(fon, rusSentence)
        if fonValue is None:
            raise Exception('No fon element for fonWord %s with id: %s, sentence: %s' % (fonWordId, fonToken, rusSentence))
        
        if gloss is None:
            raise Exception('No gloss element for fonWord %s with id: %s, sentence: %s' % (fonWordId, fonToken, rusSentence))
        
        glossValue = getAnnotationValueFromElement(gloss, rusSentence)
        if glossValue is None:
            raise Exception('No gloss element for fonWord %s with id: %s, sentence: %s' % (fonWordId, fonToken, rusSentence))
        analysis.append({'fon' : fonValue, 'gloss': glossValue})
    return analysis



def getPos(root, fonWord):
    fonWordId = getElementId(fonWord)
    posEl = getPosById(root, fonWordId)
    if posEl is None:
        return None
    return encodePOS(getAnnotationValueFromElement(posEl))
    
    
def getRoot(filename):
    tree = ET.parse(filename)
    return tree.getroot()


def getSentences(root, languageCode):
    languageXpathWithCode = LANGUAGE_XPATH % languageCode
    return root.findall(languageXpathWithCode)


def getAnnotationValueFromElement(element, rusSentence = None):
    elementText = element.find('.' + ANNOTATION_VALUE_XPATH).text
    if elementText:
        return elementText.strip()
    errorText = 'Empty element found'
    if rusSentence is not None:
        errorText += ' for sentence %s' % rusSentence
    raise Exception(errorText)


def getElementId(element):
    return element.attrib[ANNOTATION_ID_ATTRIBUTE]

def getFonWordsById(root, annotationId):    
    return root.findall(FONWORD_XPATH + "[@" + 
                      ANNOTATION_REF_ATTRIBUTE +  
                      "='" + annotationId+ "']");
        
        
def getFonsById(root, annotationId):
    return root.findall(FON_XPATH + "[@" + 
                      ANNOTATION_REF_ATTRIBUTE +  
                      "='" + annotationId+ "']");
                      
                      
def getPosById(root, annotationId):
    return root.find(POS_XPATH + "[@" + 
                      ANNOTATION_REF_ATTRIBUTE +  
                      "='" + annotationId+ "']");                      
                      
                      
def getGlossById(root, annotationId):
    return root.find(GLOSS_XPATH + "[@" + 
                      ANNOTATION_REF_ATTRIBUTE +  
                      "='" + annotationId+ "']");
                      

def encodePOS(posFromEaf):
    if posFromEaf in POS_CONVERSION:
        return POS_CONVERSION[posFromEaf]
    raise Exception("no such pos:" + posFromEaf)

        
