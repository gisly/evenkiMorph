# coding=utf-8
import codecs
import os
from zaliznyakDB import ZaliznyakDB

__author__ = 'gisly'

ZALIZNYAK_FOLDER='E:\\LingM\\Zaliznyak\\dict\\'

Z_NOUN=[u'м', u'ж',u'с',u'мо', u'жо',u'со',u'мн.' ]
Z_VERB=[u'св',u'нсв', u'св-нсв']
Z_ADJ=[u'п']
Z_NUM=u'числ.'
Z_ADV=[u'н']

M_NOUN='Nindps'
M_VERB='Verb'
M_ADJ='Adj'
M_NUM='Num'
M_ADV='Adv'


db=ZaliznyakDB()

def zaliznyakToMongo():
    for filename in os.listdir(ZALIZNYAK_FOLDER):
        zaliznyakFileToMongo(ZALIZNYAK_FOLDER+'\\'+filename)
        print 'processed '+filename

def zaliznyakFileToMongo(filename):
    with codecs.open(filename, 'r', 'utf-8') as fin:
        for line in fin:
            lineParts=line.split(' ')
            if len(lineParts)>1:
                pos=lineParts[2]
                if pos in Z_NOUN:
                    insertIntoMongo(lineParts[0], M_NOUN)
                elif pos in Z_VERB:
                    insertIntoMongo(lineParts[0], M_VERB)
                elif pos in Z_ADJ:
                    insertIntoMongo(lineParts[0], M_ADJ)
                elif pos.startswith(Z_NUM):
                    insertIntoMongo(lineParts[0], M_NUM)

                elif pos in Z_ADV:
                    insertIntoMongo(lineParts[0], M_ADV)

def insertIntoMongo(word, pos):
    db.insertWord({'word':word, 'pos':pos})


zaliznyakToMongo()