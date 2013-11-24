# coding=utf-8
__author__ = 'gisly'
import re
import codecs
import tkMessageBox
from Tkconstants import END
import Tkinter
import tkFileDialog
from evenkiMorphProcessor import EvenkiMorphProcessor
from cyrillicToLatin import cyrToIPA

class MorphVis(object): 
    
    UNKNOWN='+?'
    
    RES_DELIM='\n'
    RES_WORD_DELIM = '\t'
    LINE_DELIM='\r\n'

    
    MORPH_RES = 'morph'
    MORPH_RES_BG = 'green'
    
    TRANSLATION_MARK = '__RUS__'
    
    ENTRY_WIDTH=50
    
    

    def initVisualizer(self):
        self.evenkiMorphProcessor = EvenkiMorphProcessor()
        self.initControls()

    def initControls(self):
        self.root = Tkinter.Tk()
        
        controlPanel = Tkinter.Frame(self.root)
        controlPanel.pack(side="right")
        
        
        
        morphButton=Tkinter.Button(controlPanel, text= "run analyzer",
            command=self.onProcess)
        morphButton.pack(side="right")
        
        clearButton=Tkinter.Button(controlPanel, text= "clear all",
            command=self.onClearAll)
        clearButton.pack(side="bottom")
        
        openFileButton=Tkinter.Button(controlPanel, text= "open file",
            command=self.onOpenFile)
        openFileButton.pack(side="left")
        
        self.textWidget = Tkinter.Text(self.root, width=self.ENTRY_WIDTH,
            font=("Times", 12, "bold"))
        self.textWidget.pack(side="top")
        self.textWidget.tag_config(self.MORPH_RES, background=self.MORPH_RES_BG)

        self.textWidget.tag_bind(self.MORPH_RES, "<Button-1>", self.showAnalysis)
        
        '''self.rusTextWidget = Tkinter.Text(self.root, font=("Times", 10))
        self.rusTextWidget.pack(side="bottom")'''


        
        self.morphLB = Tkinter.Listbox(self.root, width=self.ENTRY_WIDTH)
        self.morphLB.pack(side="left")
        
        self.root.mainloop()
        
    def showAnalysis(self, event):
        index = self.getTkinterIndexByClickEvent(event)
        [begOfWord, endOfWord]  = self.getBegOfWordEndOfWordByIndex(index)
        self.curBeg = begOfWord
        self.curEnd = endOfWord
        word = self.getTokenByIndices(begOfWord, endOfWord)
        wordRes = self.getRes(word)
        self.addToLB(wordRes)
    
    def onProcess(self):
        text = self.getInputText()
        tokenizedText = self.tokenize(text)
        tokenizedLatin = self.cyrToLatin(tokenizedText)
        res = self.evenkiMorphProcessor.callProcessorText(tokenizedLatin)
        self.processRes(res)
        
    def onOpenFile(self):
        filename = tkFileDialog.askopenfilename()
        if len(filename) > 0:
            self.processFilename(filename)            
    
            
    def onClearAll(self):
        self.clearListbox()
        self.clearTextWidget()
        
        
    def processFilename(self, filename):
        text = self.readFile(filename)
        textParts = text.split(self.TRANSLATION_MARK)
        self.displayText(textParts[0])
        '''if len(textParts)>1:
            self.displayText(textParts[1], isEv=False)''' 
        
    def processRes(self, res):
        self.res = dict()
        for word, analysis in res.items():
            analysisRes = analysis.strip().decode('utf-8').split(self.RES_DELIM)
            if not self.isUnknown(analysisRes):
                analysisRes = [resPart.split(word, 1)[1] for resPart in analysisRes]
                cyrWord = self.latCyr[word]
                self.res[cyrWord] = analysisRes
                self.highlight_pattern(cyrWord, self.MORPH_RES)
                
        
    def getRes(self, word):
        return self.res.get(word)
        
    def getInputText(self):
        return self.textWidget.get("1.0", END)
    
    
    def displayText(self, text):
        self.clearTextWidget()
        self.textWidget.insert(END, text)
        '''if isEv:
            self.clearTextWidget()
            self.textWidget.insert(END, text) 
        else:
            self.clearRusTextWidget()
            self.rusTextWidget.insert(END, text)''' 
        
    def clearTextWidget(self):
        self.textWidget.delete("1.0", END) 
    
    def clearRusTextWidget(self):
        self.rusTextWidget.delete("1.0", END) 
    
    def addToLB(self, wordRes):
        self.clearListbox()
        if wordRes:
            for item in wordRes:
                self.morphLB.insert(END, item)

    def clearListbox(self):
        self.morphLB.delete(0, END)
       
        
    def tokenize(self, text):
        return re.split(ur' |\,|-|\.|\r\n', text.strip())
    
    def cyrToLatin(self, tokenizedText):
        self.latCyr = dict()
        latRes = []
        for word in tokenizedText:
            word = word.strip()
            latWord = cyrToIPA(word)
            self.latCyr[latWord]=word
            latRes.append(latWord)
        return latRes

    def isUnknown(self, res):
        return self.UNKNOWN in res[0]
    
        
        
    
    ###############WORD INDICES################

    def getBegOfWordEndOfWordByIndex(self, index):
        begOfWord = self.textWidget.search(",|\.| |\r\n|-", index, stopindex="1.0", regexp=True,
            backwards=True)
        if begOfWord == "":
            begOfWord = "1.0"
        '''else:
            begOfWord = "%s+1c" %  begOfWord'''
        endOfWord = self.textWidget.search(",|\.| |\r\n|-", index, stopindex=END, regexp=True)
        if endOfWord == "":
            endOfWord = END
        else:
            endOfWord = "%s+1c" %  endOfWord
        return [begOfWord, endOfWord]

    def getTokenByIndices(self, begOfWord, endOfWord):
        return self.textWidget.get(begOfWord, endOfWord).strip('.').strip('-').strip()

    def getTkinterIndexByClickEvent(self, event):
        return self.textWidget.index("@%s,%s" % (event.x, event.y))


    def highlight_pattern(self, pattern, tag, start="1.0", end="end"):
        #TODO: simplify
        start = self.textWidget.index(start)
        end = self.textWidget.index(end)
        self.textWidget.mark_set("matchStart",start)
        self.textWidget.mark_set("matchEnd",start)
        self.textWidget.mark_set("searchLimit", end)

        count = Tkinter.IntVar()
        pattern = self.escape(pattern)
        while True:
            index = self.textWidget.search("(\s|\r\n|-)?"+pattern+"(\s|\.|^|\r\n|-)?", "matchEnd","searchLimit",
                count=count, regexp=True)
            if index == "": break
            self.textWidget.mark_set("matchStart", index)
            self.textWidget.mark_set("matchEnd", "%s+%sc" % (index,count.get()))
            self.textWidget.tag_add(tag, "matchStart","matchEnd")
            
    def escape(self, text):
        return text.replace('.','\.')


    def readFile(self, filename):
        with codecs.open(filename, 'r', 'utf-8') as fin:
            return fin.read()
    
def main():
    MorphVis().initVisualizer()
    
if __name__ == "__main__":
    main()