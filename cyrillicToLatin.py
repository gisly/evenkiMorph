#encoding=utf-8

import codecs
import sys

vowels=[u'а',u'е',u'ё',u'и',u'о',u'у',u'ы',u'э',u'ю',u'я']
consonants=[u'б',u'в',u'г',u'ж',u'з',u'к',u'л',u'м',u'п',u'р',u'т',u'ф',u'х',u'ц',u'ч',u'ш',u'щ']
iotisedVowels={u'е':u'e',u'ё':u'о',u'ю':u'u',u'я':u'a'}

pairs_to_pairs = {




    u'де': u"d'e",
    u'дё': u"d'o",
    u'дю': u"d'u",
    u'дя': u"d'a",


    u'се': u"s'e",
    u'сё': u"s'o",
    u'сю': u"s'u",
    u'ся': u"s'a",

    u'не': u"n'e",
    u'нё': u"n'o",
    u'ню': u"n'u",
    u'ня': u"n'a",

    u'те': u"t'e",
    u'тё': u"t'o",
    u'тю': u"t'u",
    u'тя': u"t'a"

}
lower_case_letters = {
    u'…':'',
    '.':'',
    u'«':'',
    u'»':'',
    u',':'',
    u':':'',
    '"':'',
    u' — ':'',
    '?':'',
    '!':'',

    u'а': u'a',
    u'б': u'b',
    u'в': u'w',
    u'г': u'g',
    u'д': u'd',
    u'е': u'je',
    u'ё': u'jo',
    u'ж': u'zh',
    u'з': u'z',
    u'и': u'i',
    u'й': u'j',
    u'к': u'k',
    u'л': u'l',
    u'м': u'm',
    u'н': u'n',
    u'ӈ' : u'ng',
    u'о': u'o',
    u'п': u'p',
    u'р': u'r',
    u'с': u's',
    u'т': u't',
    u'у': u'u',
    u'ф': u'f',
    u'х': u'h',
    u'ц': u'ts',
    u'ч': u'ch',
    u'ш': u'sh',
    u'щ': u'sch',
    u'ъ': u'',
    u'ы': u'i',
    u'ь': u'',
    u'э': u'e',
    u'ю': u'ju',
    u'я': u'ja'
}




def cyrToIPA(s):
    '''converts a cyrillic string into an ASCII fonetic string'''
    s=s.lower()
    for cyr, IPA in pairs_to_pairs.iteritems():
        s=s.replace(cyr, IPA)

    for cons in consonants:
        for vowel,vowelRep in iotisedVowels.iteritems():
            s=s.replace(cons+vowel, cons+vowelRep)

    for lower_case_letter, lower_case_letter_IPA in lower_case_letters.iteritems():
        s=s.replace(lower_case_letter, lower_case_letter_IPA)

    return s
def main():
    if len(sys.argv)<2:
        raise Exception('no input file name specified')
    inputFileName=sys.argv[1]
    if len(sys.argv)<3:
        outputFileName=inputFileName+'_out.txt'
    else:
        outputFileName=sys.argv[2]
    with codecs.open(inputFileName, 'r', 'utf-8') as fin:
        text=fin.read()
    with codecs.open(outputFileName, 'w', 'utf-8') as fout:
        fout.write(cyrToIPA(text))

if __name__ == "__main__":
    main()