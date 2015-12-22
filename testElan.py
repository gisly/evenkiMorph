# coding=utf-8
__author__ = 'gisly'


import os

import eaf_utils
from evenkiMorphProcessor import EvenkiMorphProcessor
from cyrillicToLatin import replaceSpecialSymbols

LANGUAGE_CODE = 'ev'
LANGUAGE_CODE_RUS = 'rus'
IS_TO_USE_FON = False


OMITTED_GLOSS_LIST = ['sg', 'nom', 'n', 'v' , 'adj', 'adv']
GLOSS_MAPPING = {u'_я':'_1sg', u'_он': '_3sg', u'imper3sg':'imper.3sg',
                 u'imper2sg':'imper.2sg',
                 
                 u'imper1sg':'imper.1sg',
                 u'evid':u'prob',
                 u'ela':u'elat',
                 u'nginakin':'nginaki',
                 u'kungakan':'kungaka',
                 u'chipkan':'chipka',
                 
                  u'_самка':u'_женщина',
                 u'_замечательный':u'_хороший', u'_унести':u'_пойти', u'_жердь':u'_дерево',
                 u'_увидать': u'_видеть', u'_сбегать':u'_убежать', u'_деготь':u'смола',
                 u'_дёготь':u'смола', u'_воротиться':u'_вернуться'}
DERIVATIVE_GLOSSES = [u'atten', 'ints', 'nmlz.temp']

DICTIONARY_NORMALIZED = {u'человек.мужчина':u'человек', 
                         u'neg':u'отсутствие', 
                         u'курить' : u'стянуть',
                         u'дышать':u'надышаться',
                         u'давнее.время':u'век',
                         u'сбегать':u'убежать',
                         u'advz':u'instr',
                         u'настать(о.лете)':u'лето',
                         u'берег':u'побережье',
                         u'жить':u'прожить',
                         u'плыть.по.течению':u'хлынуть',
                         u'грести.веслами':u'грести',
                         u'лодка.берестянка':u'лодка'
                         }


processor = EvenkiMorphProcessor()


def parseElanFolderWithParser(elanFolder):
    totalEafFileNum = 0
    totalTokens = 0
    goodParses = 0
    
    
    
    for root, dirs, files in os.walk(elanFolder):   
        for filename in files:
            fullFilename = os.path.join(root, filename)
            
            
                
            
            if isGoodElanFileName(fullFilename):
                totalEafFileNum += 1
                try:
         
                    (totalNum, goodNum) = parseElanFileWithParser(fullFilename, LANGUAGE_CODE)
                    totalTokens += totalNum
                    goodParses += goodNum
                except Exception, e:
                    print str(e)
                
    print 'TOTAL:%s, GOOD:%s' % (totalTokens, goodParses)
                
    
def isGoodElanFileName(filename):
    return filename.endswith('transliterated.eaf')

def parseElanFileWithParser(elanFilename, languageCode):
    print elanFilename
    
    textInfo = eaf_utils.getTextInfo(elanFilename, languageCode, IS_TO_USE_FON, False)
    tokenList = getTokenList(textInfo)
    
    
    tokenValuesAsList = getTokenValuesAsList(tokenList)
    
    """for token in tokenList:
        print token
        
        tokenValue = token['token']
        tokenGloss = token['analysis']
        automaticResult = processor.callProcessorText([tokenValue])
        print automaticResult"""
        
    result = processor.callProcessorListOfWords(tokenValuesAsList)
    
    
    
    totalTokenNum = len(tokenList)
    goodAnalyses = 0
    
    for index, token in enumerate(tokenList):
        tokenAnalysisAutomatic = result[index]
        tokenAnalysisManual = token['analysis']

        
        comparisonResult = compareAnalyses(tokenAnalysisAutomatic, tokenAnalysisManual)
        if comparisonResult:
            goodAnalyses += 1
            
            
    print 'TOTAL:%s, GOOD:%s' % (totalTokenNum, goodAnalyses)
    return (totalTokenNum, goodAnalyses)
        

    
def compareAnalyses(automaticAnalysis, manualAnalysis):
    manualNormalized = normalizeManualAnalysis(manualAnalysis)
    
    
    automaticAnalysisList = automaticAnalysis.strip().split('\n')
    automaticAnalysisListNormalized = [normalizeAutomaticAnalysis(analysisVariant) 
                                       for analysisVariant in automaticAnalysisList]
    
    

    result = manualNormalized in automaticAnalysisListNormalized
    
    
    if not result and not u'+?' in automaticAnalysisListNormalized:
        print 'MANUAL:' + manualNormalized
        for automaticAnalysisVariant in automaticAnalysisListNormalized:
            print automaticAnalysisVariant
        
            print '========'
    
    return result
     
     
def normalizeManualAnalysis(manualAnalysis):   
    manualPrefix = manualAnalysis[0]['fon']
    for morpheme in manualAnalysis:
        if isDerivativeGloss(morpheme['gloss']):
            manualPrefix += morpheme['fon'].replace('-', '')
    
    manualPrefix = replaceSpecialSymbols(manualPrefix)
    
    return ('+'.join([manualPrefix] + [normalizeGloss(morpheme['gloss']) for morpheme in manualAnalysis[1:] if 
                                                      not isDerivativeGloss(morpheme['gloss'])])).lower()
    
    """return (manualPrefix + '_' + '+'.join([normalizeGloss(morpheme['gloss']) for morpheme in manualAnalysis if 
                                                      not isDerivativeGloss(morpheme['gloss'])])).lower()"""

def normalizeGloss(gloss):
    if gloss.lower() in DICTIONARY_NORMALIZED:
        return DICTIONARY_NORMALIZED[gloss.lower()]
    return gloss


def isDerivativeGloss(manualGloss):
    return manualGloss.lower() in DERIVATIVE_GLOSSES

def normalizeAutomaticAnalysis(automaticAnalysis):
    automaticAnalisysVariant = automaticAnalysis.split('\t')[-1].strip().lower()
    
    glossParts = automaticAnalisysVariant.split('+')
    
    
    glossPartsJoined = '+'.join([normalizeAutomaticGloss(gloss) for gloss in glossParts if gloss not in OMITTED_GLOSS_LIST])
    
    

        
    for glossMapping, glossMappingValue in GLOSS_MAPPING.iteritems():
        glossPartsJoined = glossPartsJoined.replace(glossMapping, glossMappingValue)
        
    return replaceSpecialSymbols(glossPartsJoined)

def normalizeAutomaticGloss(gloss):
    return gloss.split('_')[0]



def getTokenList(textInfo): 
    tokenList = []
    for sentence in textInfo:
        tokenList += sentence['morphology']
    return tokenList

def getTokenValuesAsList(tokenList):
    return [token['token'] for token in tokenList]
