# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 09:50:33 2016

@author: Erman
"""


import math

    
with open('debate1_trump_vs_clinton.txt','r') as infile:
    text_in=infile.read()
    
split_nl=text_in.split("\n")

#sentiment

with open('word_scores.txt','r') as infile:
    text_in=infile.readlines()
   

ii=0
sentDict={}

for str in text_in:
    oneSent=str.split("\n")
    oneSentString=oneSent[0]
    sss=oneSentString.split("\t")
    sentDict[sss[0]]=int(sss[1])
    
def getSentimentValue(tweet,sentDictionary):
    sentSum=0
    tweet=tweet.split()
    for word in tweet:
        word=word.lower()
        if sentDictionary.has_key(word):
            sentSum+=sentDictionary[word]
    return sentSum;



def getTweetSentDict(tweets,sentDictionary):
    tweetSentValues={}
    for tw in tweets:
        if tw not in tweetSentValues:
            tweetSentValues[tw]=getSentimentValue(tw,sentDictionary)

    return tweetSentValues

twValues=getTweetSentDict(split_nl,sentDict)

def getHashDict(tweets):
    hashDict={}
    
    for tw in tweets:
        tw2=tw.split()
        for word in tw2:
            if word[0]=='#':
                if tw not in hashDict:
                    hashDict[tw]=[word]
                else:
                    hashDict[tw].append(word)
                  
    return hashDict      
    
hashDict=getHashDict(split_nl)


def getReverseHash( hashDict):
    reverseHash={}
    for tw in hashDict:
        hashList=hashDict[tw]
        for hsh in hashList:
            if hsh not in reverseHash:
                reverseHash[hsh]=[tw]
            else:
                reverseHash[hsh].append(tw)
    return reverseHash

rHashDict=getReverseHash(hashDict)

def getHashSents(reverseHash,tweetValDict):
    hashSentDict={}
    hashCountDict={}
    for hsh in reverseHash:
        tweets=reverseHash[hsh]
        count=len(tweets)
        sum=0
        for tw in tweets:
            sum+=tweetValDict[tw]
        value=float(sum)/count
        hashSentDict[hsh]=value
        hashCountDict[hsh]=count
    return[hashSentDict,hashCountDict]
            
[hashSentD,hashCountD]=getHashSents(rHashDict,twValues)      



def filterDicts(hSentD,hCountD,cutoff):
    hashSentDictF={}
    hashCountDictF={}

    for hsh in hSentD:
        if abs(hSentD[hsh])>=cutoff:
            hashSentDictF[hsh]=hSentD[hsh]
            hashCountDictF[hsh]=hCountD[hsh]

    return [hashSentDictF,hashCountDictF]

cutoff=7.0
[hashSentDF,hashCountDF]=filterDicts(hashSentD,hashCountD,cutoff)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sent_series = pd.Series.from_array(hashSentDF.values()) 


plt.figure(figsize=(102, 15))
ax = sent_series.plot(kind='bar')

ax.set_xlabel("#HashTags")
ax.set_ylabel("Sentiment Value")

rects = ax.patches
labels =hashSentDF.keys()

for rect, label in zip(rects, labels):
    height = 1.1*hashSentDF[label]
    ax.text(rect.get_x() + rect.get_width()/2, height , label, ha='center', va='bottom')

    
    
    
   