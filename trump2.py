# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 21:46:15 2016

@author: Erman
"""


import math 
from nltk.corpus import stopwords
from random import randint


stop1 = set(stopwords.words('english'))
stop2=["i","he's","she's","it's","i'm","don't","that's","can't","it","  ","I", "i "," i","a","the","to","is","she","but","we","and","has","of","in","that","this","of","not"]



with open('debate1_trump_vs_clinton_yucel_win.txt','r') as infile:
    text_in=infile.read()
    
split_nl=text_in.split("\n")

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


idList,pDict, worddDict=getDicts(split_nl)


def ejectMan(id,pDict,wDict):
    
    
    oneman=pDict.pop(id)

        
    for word in oneman:
        wDict[word]=wDict[word]-oneman[word]
    return [pDict,wDict]


def ejectRandomMan(idList,pDict,wDict):
    length=len(idList)
    nu= randint(0,length)
    id=idList[nu]
    
    pDict,wDict=ejectMan(id,pDict,wDict)
    return [id,pDict,wDict]
    
def getCommonWord(number,pDict):
    list1=[]

    for id in pDict:
        dummy=pDict[id]
        for word in dummy:
            list1.append(dummy[word])
            
    list1.sort(reverse=True)
   
    topCommon=list1[1:number]

    return topCommon

def getUnCommonWord(number,pDict):
    list1=[]

    for id in pDict:
        dummy=pDict[id]
        for word in dummy:
            list1.append(dummy[word])
            
    list1.sort()
   
    topCommon=list1[1:number]

    return topCommon    
    
    
def totalNoise(wordDict,values,delta):
    import numpy as np
    list3=[]
    newDict={}
    rDict=getReverseDict( wordDict)
    epsilon=(1/len(values))
    
    
    for val in values:
        noise=int(np.random.laplace(delta*epsilon))
        print noise
        word=rDict[val][0]
        val+=noise
        list3.append(val)
        if word not in newDict:
            newDict[word]=val
    list3.sort(reverse=True)
    return list3,newDict




def getReverseDict( wDict):
    reverseDict={}
    for word in wDict:
        wValue=wDict[word]
        if wValue not in reverseDict:
            reverseDict[wValue]=[word]
        else:
            reverseDict[wValue].append(word)
    return reverseDict
    
def getCommonWords(maxNum,wordDict):    
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
 

def getUnCommonWords(maxNum,wordDict):    
    wordValues=worddDict.values()
    
    
    wordValues.sort()
    wordValues=wordValues[0:maxNum]
    
    RevDict=getReverseDict( worddDict)
    CommonWordList=[]
    
    for ii in range(maxNum):
        word=RevDict[wordValues[ii]]
        if word not in CommonWordList:
            CommonWordList.append( RevDict[wordValues[ii]])    
            
    return [CommonWordList,wordValues]




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
    
#    for rect, label in zip(rects, labels):
#        height=wordValues[i]
##        height =1.1* worddDict[label[0]]
#        ax.text(rect.get_x() + rect.get_width()/2, height , label[0], ha='center', va='bottom')
#        i=i+1

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
            


#############################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

maxNum=50
[CommonWordList,wordValues]=getCommonWords(maxNum,worddDict)
    

    
#Word Cloud
reverseDictionary1=getReverseDict(worddDict)
plotBars("Words","Number of Occurances",wordValues,CommonWordList,worddDict,reverseDictionary1)

#Add Noise
mostNum=10
mostUsed=getCommonWord(mostNum,pDict)
delta1=mostUsed[0]
leastUsed=getUnCommonWord(mostNum,pDict)
delta2=leastUsed[0]
delta=delta1-delta2
factor=5

tnoised1,newDict1=totalNoise(worddDict,wordValues,factor,delta) 
reverseDictionary2=getReverseDict(newDict1)
   
plotBars("Words","Number of Occurances",tnoised1,CommonWordList,newDict1,reverseDictionary2)

##################################################
## Queries


print differenceQuery("trump",worddDict,newDict1)   


iddd,pDictEjected,worddDictEjected= ejectRandomMan(idList,pDict,worddDict) 

