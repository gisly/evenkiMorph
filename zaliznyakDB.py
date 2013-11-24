# coding=utf-8
import pymongo

__author__ = 'gisly'

class ZaliznyakDB:

    def __init__(self,host='localhost',port=27017,dbName='zaliznyak'):
        self.connection=pymongo.Connection(host,port)
        self.db=self.connection[dbName]
    def __del__(self):
        self.connection.close()

    def insertWord(self, wordPos):
        colWords=self.db.wordsPos
        colWords.insert(wordPos)

    def insertEvenkiWord(self, evenkiWord):
        colWords=self.db.evenkiDict
        colWords.insert(evenkiWord)

    def getEvenkiWordsByPos(self, wordPos):
        colEvenkiDict=self.db.evenkiDict
        return colEvenkiDict.find({'pos':wordPos})

    def getEvenkiWords(self):
        colEvenkiDict=self.db.evenkiDict
        return colEvenkiDict.find().sort("pos",1)

    def getEvenkiWordsByWord(self, word):
        colEvenkiDict=self.db.evenkiDict
        return colEvenkiDict.find(word)

    def updateEvenkiWord(self, word):
        self.db.evenkiDict.update({'_id':word['_id']}, word, upsert=True)

    def fff(self):
        '''word=dict()
        word["evenki"]=u"хокторо̄н "
        word["rus"]=u'старая тропа'
        word["pos"]="Nindps"
        self.db.evenkiDict.insert(word)'''


        '''words = self.db.evenkiDict.find({"pos":"Vvoice","rus":{'$regex':u'.*[a-z]+.*'}})
        for word in words:

            rusWords = self.db.evenkiDict.find({"pos":"Vvoice","ipa":word['ipa'],"rus":{'$regex':u'.*[а-я]+.*'}})
            flag=False
            for rusWord in rusWords:
                flag=True
                print rusWord['rus']
                self.db.evenkiDict.remove(word)
            if not flag:
                print word['evenki']+'_'+word['rus']  '''

        '''words = self.db.evenkiDict.find({"pos":"Vvoice","ipa":{'$regex':u'^s-h.*\[.*'}})
        for word in words:
            print word['evenki']
            try:
                word['evenki'] = word['evenki'].split(' ',1)[1]
                print word['evenki']
                #self.db.evenkiDict.update({'_id':word['_id']},word,  upsert=False)
            except Exception, e:
                pass '''


        '''wordsWithRazg =       self.db.evenkiDict.find({"pos":"Vvoice", "ipa":{'$regex':u"razg"}})

        for wordWithRazg in wordsWithRazg:
            print 'razg:'+wordWithRazg['evenki']'''



        '''words=self.db.evenkiDict.find({"pos":"Vvoice", "ipa":{'$regex':".*d'o$"}})
        for word in words:
            try:
                verbRoot = word['ipa'].split('[')[0].strip()[0:-3]
                verbEvenkiRoot= word['evenki'].split('[')[0].strip()[0:-2]
                if len(verbEvenkiRoot)>1:
                    print    word['ipa']
                    print verbRoot
                    wordsWithThisRoot =  self.db.evenkiDict.find({"pos":"Vvoice", "ipa":verbRoot})
                    flagIsFound = False
                    print '=================='
                    for sameRootVerb in wordsWithThisRoot:
                        sameRootVerb['vht']='Otype'
                        flagIsFound = True
                        #self.db.evenkiDict.update({'_id':sameRootVerb['_id']},sameRootVerb,  upsert=False)
                    if not flagIsFound:
                        print 'not found:'+verbRoot
                        newWord = dict()
                        newWord['evenki'] = verbEvenkiRoot
                        newWord['rus'] = word['rus']
                        newWord['pos'] = 'Vvoice'
                        newWord['vht']='Otype'
                        #self.db.evenkiDict.insert(newWord)

                    self.db.evenkiDict.remove(word)
                else:
                    print 'too short:'+verbEvenkiRoot
            except Exception, e:
                print 'exception:'+str(e) '''




                #self.db.evenkiDict.update({'_id':word['_id']},word,  upsert=False) '''

        '''words=self.db.evenkiDict.find({"evenki":u"поэт.[/c][/i][/p] омолги"})
        for word in words:
            word["evenki"]=u"поэт.[/c][/i][/p] омолгӣ"
            self.db.evenkiDict.update({'_id':word['_id']},word,  upsert=False)'''
        '''self.db.evenkiDict.remove({'evenki':''})
        self.db.evenkiDict.remove({'evenki':{'$regex':'.*\\d\\..*'}})
        self.db.evenkiDict.remove({'evenki':{'$regex':'\\d'}})
        self.db.evenkiDict.remove({'evenki':'разг.[/c][/i][/p]'})
        vhtWords=self.db.evenkiDict.find({'vht':'Atype'})'''

        '''word=dict()
        word["evenki"]=u"экӣн"
        word["rus"]=u'старшая_сестра'
        word["pos"]="Nindps"
        self.db.evenkiDict.insert(word)'''
        #self.db.evenkiDict.update({"evenki":u"дявавча̄"},{"evenki":u"дявавча̄", "rus":u"занятый", "pos":"Adj", "vht":"Etype"},  upsert=False)
        #self.db.evenkiDict.remove({"rus":u"(быть занятым) хавалдя-мӣ; я занят би хавалдям"})
        #self.db.evenkiDict.update({"evenki":u"няӈна"},{"evenki":u"няӈня"},  upsert=False)

ZaliznyakDB().fff()


