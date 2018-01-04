# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:51:12 2017

@author: Erman
"""

import math 
from nltk.corpus import stopwords
from random import randint
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

stop1 = set(stopwords.words('english'))
stop2=["i","he's","she's","it's","i'm","don't","that's","can't","it","  ","I", "i "," i","a","the","to","is","she","but","we","and","has","of","in","that","this","of","not"]





def checkPunctuation(letter):
    if letter=='.' or letter==',' or letter=='?' or letter=='!' or letter=='"' or letter==':'or letter==' 'or letter==';':
        return True
    else:
        return False
    
        
def cleanUpPunct(word):
    letterList=""
    for ii in range(len(word)):
        if not checkPunctuation(word[ii]):
            letterList=letterList+word[ii]
            
    return letterList
    
    
    

def getDicts(split):
    personDict={}
    wordDict={}
    idList=[]
    
    stop1 = set(stopwords.words('english'))
    stop2=["i","he's","she's","it's","i'm","don't","that's","can't","it","  ","I", "i "," i","a","the","to","is","she","but","we","and","has","of","in","that","this","of","not"]

    
    for tweet in split:
        
        
        tweet=tweet.split("\t")
        idd=tweet[0]
        phrase=tweet[1]
        
        dummy={}
        if idd not in personDict:
            personDict[idd]=dummy
            idList.append(idd)
    
        phrase=phrase.split()
        for word in phrase:
            word=word.lower()
            word=cleanUpPunct(word)
            if word not in stop1 and word not in stop2  :
                                
                wDict=personDict[idd]
                if not(word=="" or word=="-"):
                    if wDict.has_key(word):
                        wDict[word]+=1
                    else:
                        wDict[word]=1 
                    
                    personDict[idd]=wDict
                    
                    if wordDict.has_key(word):
                        wordDict[word]+=1
                    else:
                        wordDict[word]=1 
                
    return [idList,personDict, wordDict]



def differenceQuery(word,dict1,dict2):
    
    try:
        value=dict2[word]-dict1[word]
    except:
        return 0
    
    return value

    

def plotBars(xlabel,ylabel,wordValues,CommonWordList,worddDict,rDict):
    
    sent_series = pd.Series.from_array(wordValues) 


    plt.figure(figsize=(102, 15))
    ax = sent_series.plot(kind='bar')
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    rects = ax.patches
    labels = []
    i=0
#    label=""

    for rect in rects:
            height=wordValues[i]
            try:
                words=rDict[height]
                for word in words:
                    if word not in labels:
                        labels.append(word)
                        label=word
                        break
            except:
                print ""
            ax.text(rect.get_x() + rect.get_width()/2, height , label, ha='center', va='bottom')
            i=i+1
            
            
            
            
def getReverseDict( wDict):
    reverseDict={}
    for word in wDict:
        wValue=wDict[word]
        if wValue not in reverseDict:
            reverseDict[wValue]=[word]
        else:
            reverseDict[wValue].append(word)
    return reverseDict
    
def getCommonWords(maxNum,worddDict):    
    wordValues=worddDict.values()
    
    
    wordValues.sort(reverse=True)
    wordValues=wordValues[0:maxNum]
    
    RevDict=getReverseDict( worddDict)
    CommonWordList=[]
    
    for ii in range(maxNum):
        word=RevDict[wordValues[ii]]
        if word not in CommonWordList:
            CommonWordList.append( RevDict[wordValues[ii]])    
            
    return [CommonWordList,wordValues]

def getMaxWPerP(word,pDict):
    occurrance=0
    
    for dictionary in pDict:
        personListDict=pDict.values()
        for dictionary2 in personListDict:
            try:
                
                number=dictionary2[word]
            except:
                number=0
#            print number  
            if number>occurrance:
                occurrance=number
    
    return occurrance
    
def getMaxWPerP(word,pDict):
    occurrance=0
    
    for dictionary in pDict:
        personListDict=pDict.values()
        for dictionary2 in personListDict:
            try:
                
                number=dictionary2[word]
            except:
                number=0
#            print number  
            if number>occurrance:
                occurrance=number
    
    return occurrance
    
def totalNoise2(wordDict,commonWordList,epsilon,pDict):
    import numpy as np
    newDict=wordDict.copy()
    epsilon=1.0*epsilon/len(commonWordList)
    for wList in commonWordList:
        
        for word in wList:
            
            delta=getMaxWPerP(word,pDict)
            noise=math.fabs(np.random.laplace(delta,1/epsilon))
#            factor=math.fabs(np.random.laplace(0,epsilon))
            #factor=math.fabs(delta*epsilon)

            print newDict[word]
            newDict[word]+=int(noise)
#            print newDict[word]
            print noise
    return newDict

#######################################

with open('debate1_trump_vs_clinton_yucel_win.txt','r') as infile:
    text_in=infile.read()
    
split_nl=text_in.split("\n")
idList,pDict, worddDict=getDicts(split_nl)

epsilon=0.01

maxNum=20
#Original
[CommonWordListOr,wordValuesOr]=getCommonWords(maxNum,worddDict)

reverseDictionaryOr=getReverseDict(worddDict)
plotBars("Words","Number of Occurances",wordValuesOr,CommonWordListOr,worddDict,reverseDictionaryOr)

#Noised
newDictOrNoised=totalNoise2(worddDict,CommonWordListOr,epsilon,pDict)

[CommonWordListOrNoised,wordValuesOrNoised]=getCommonWords(maxNum,newDictOrNoised)
reverseDictionaryNoised=getReverseDict(newDictOrNoised)
plotBars("Words","Number of Occurances",wordValuesOrNoised,CommonWordListOrNoised,newDictOrNoised,reverseDictionaryNoised)






