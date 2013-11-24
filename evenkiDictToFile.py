# coding=utf-8
__author__ = 'gisly'
import codecs
import re
import unicodedata
from cyrillicToLatin import cyrToIPA


from zaliznyakDB import ZaliznyakDB

class EvenkiFileWriter(object):

    db=ZaliznyakDB()
    EVENKI_FOLDER='E:\\SibLang\\Evenki\\thesis\\dict\\'
    EVENKI_FILE='evenki_rus_nouns'


    LONG_VOWELS={u'ā',u'ē',u'ī',u'ō',u'ū'}
    vhtTypes={'Atype':'type1','Etype':'type2','Otype':'type3'}

    EVENKI_MORPH_LEX_INFO='E:\\SibLang\\Evenki\\thesis\\evenkiMorphLexInfo.txt'

    EXT='.lexc'
    LEXICON_HEADER='LEXICON Root\n'
    LEXICON_POS=['Noun', 'Verb']




    GLOSS_LIST=['dial[/c][/i][/p]','poet[/c][/i][/p]',
                'pril[/c][/i][/p]', 'susch[/c][/i][/p]', 'gram[/c][/i][/p]',
                'razg[/c][/i][/p]', 'peren[/c][/i][/p]',
                'voen[/c][/i][/p]', 's-h[/c][/i][/p]', 'zool[/c][/i][/p]',
                'anat[/c][/i][/p]', 'ist[/c][/i][/p]', 'ist[/c][/i][/p]',
                'sud[/c][/i][/p]', 'kants[/c][/i][/p]', 'mat[/c][/i][/p]',
                'bezl[/c][/i][/p]', 'suf[/c][/i][/p]',
                'geom[/c][/i][/p]', 't\'eh[/c][/i][/p]', 'obl[/c][/i][/p]',
                'astr[/c][/i][/p]',
                'ustar[/c][/i][/p]', 'narech[/c][/i][/p]', 'mezhd[/c][/i][/p]',
                'prostorech[/c][/i][/p]', 'soujuz[/c][/i][/p]','zh-d[/c][/i][/p]',
                'kart[/c][/i][/p]',
                'p][i][c]', '[']

    GLOSS_REGEX=r'[^| |\]]([a-z]|-)*\[/c\]\[/i\]\[/p\]'

    WORD_DELIM=' '
    
    NOUN_POS = 'Nindps'

    VERB_POS = 'Vvoice'
    
    NOUN_DECLARATION = 'LEXICON Noun\n'

    VERB_DECLARATION = 'LEXICON Verb\n'


    ################################
    ##the functions which print the dictionary out
    ################################



    def printEvenkiDictToFile(self):
        '''prints evenki rules and lexicon'''
        evenkiFileName=self.EVENKI_FOLDER+self.EVENKI_FILE
        with codecs.open(evenkiFileName+self.EXT, 'w','utf-8') as fout:
            self.printEvenkiMorphInfoToFile(fout)
            self.printEvenkiWordsToFile(fout)



    def printEvenkiWordsToFile(self,fout):
        #currently supports only nouns and verbs
        #TODO: add other parts of speech
        #get evenki nouns and verbs sorted by their translation
        fout.write(self.NOUN_DECLARATION)
        evenkiNouns=self.db.getEvenkiWordsByPos(self.NOUN_POS).sort('rus',1)
        for word in evenkiNouns:
            self.printEvenkiWordToFile(word, fout)

        fout.write(self.VERB_DECLARATION)
        evenkiVerbs=self.db.getEvenkiWordsByPos(self.VERB_POS).sort('rus',1)
        for word in evenkiVerbs:
            self.printEvenkiWordToFile(word, fout)

    def printEvenkiWordToFile(self, word, fout):
        #get the latin transcription of the word
        wordIpa=self.normalize(word['ipa'])
        #writes only one word lexemes
        if self.isOneWord(wordIpa):
            if wordIpa!='':
                if self.containsLongVowels(wordIpa):
                    #the surface representation won't contain accents
                    #but the deep representation will still have them
                    wordIpaWithoutAccents=self.strip_accents(wordIpa)
                    fout.write(self.constructDictString(wordIpaWithoutAccents, word, wordIpa))
                else:
                    fout.write(self.constructDictString(wordIpa, word))


    def printEvenkiMorphInfoToFile(self,fout):
        with codecs.open(self.EVENKI_MORPH_LEX_INFO, 'r', 'utf-8') as fin:
            text=fin.read()
        fout.write(text)



    def normalize(self,word):
        '''strips off the glosses'''
        word=re.sub(self.GLOSS_REGEX,'', word)
        word=word.replace('p][i][c]','')
        word=word.replace('[','')
        return word.strip()

    def constructDictString(self,wordIpa, word, wordIpaOld=None):
        if wordIpaOld is None:
            wordIpaOld=wordIpa
        wordLeft=[wordIpaOld]+word['rus'].split(' ')
        if 'vht' in word:
            wordIpa+=self.vhtTypes[word['vht']]
        return '_'.join(wordLeft)+':'+wordIpa+' '+word['pos']+';\n'


    def strip_accents(self,s):
        ''''the magic function which I have copy-pasted
        it finds acccent marks by their unicode properties and deletes them'''
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

    def containsLongVowels(self,word):
        for longVowel in self.LONG_VOWELS:
            if longVowel in word:
                return True
        return False

    def isOneWord(self,word):
        return not self.WORD_DELIM in word
    
    ###################
    ###the functions which help add new words to the dictionary
    ###################
    
    def updateWithTransliterationAll(self,pos=None):
        if pos:
            evenkiWords=self.db.getEvenkiWordsByPos(pos)
        else:
            evenkiWords=self.db.getEvenkiWords()
        for word in evenkiWords:
            self.updateWithTransliteration(word)


    def updateWithTransliteration(self,word):
        ipa=cyrToIPA(word['evenki'])
        word['ipa']=ipa
        self.db.updateEvenkiWord(word)


    def updateMorphTypes(self, dictFile):
        with codecs.open(dictFile, 'r', 'utf-8') as fin:
            prevLine=None
            for line in fin:

                ##the magic condition based on the broken file
                #TODO: change!
                if u'([p][i][c]вин.[/c][/i][/p]' in line and not \
                (u'девятый' in prevLine or u'изменяемость' in prevLine):
                    print prevLine

                    lineParts=line.split(u'([p][i][c]вин.[/c][/i][/p]')
                    evWord=lineParts[0].split(';')[-1].split(',')[-1].split(')')[-1].split('[m1]')[-1].split('.')[-1].strip()
                    word=dict()
                    word['rus']=prevLine.split('[m1]')[-1].split('.')[-1].split('[/m]')[0].strip()
                    word['evenki']=evWord
                    word['pos']='Nindps'
                    if not evWord in lineParts[1]:
                        evWord=evWord.split(' ')[-1]



                    vht=lineParts[1].split(evWord)[1].split(')')[0]
                    if u'а' in vht:
                        vhtType='Atype'
                    elif u'о' in vht:
                        vhtType='Otype'
                    else:
                        vhtType='Etype'

                    oldWords=self.db.getEvenkiWordsByWord(word)
                    count=0
                    word['vht']=vhtType
                    
                    self.db.db.evenkiDict.remove(word)
                    for oldWord in oldWords:

                        word['_id']=oldWord['_id']
                        self.db.updateEvenkiWord(word)
                        count+=1

                    if count==0:
                        self.db.insertEvenkiWord(word)

                prevLine=line


#EvenkiFileWriter().updateWithTransliterationAll()
#EvenkiFileWriter().printEvenkiDictToFile()
#EvenkiFileWriter().updateMorphTypes('E:\\SibLang\\Evenki\\rus_evn_evengus_tm_v01\\rus_evn_evengus_tm_v01_chng.txt')
