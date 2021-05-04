# -*- coding: utf-8 -*-
"""NLP_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s3I1b-clzUhg9EhXGgWqxw1R39H0K0eD
"""

# import packages, download wordbank, documentation resources
import nltk.data
import nltk
import spacy
from spacy import displacy
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import sys
import numpy as np
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk import Tree

#!pip install geocoder
!pip install geotext
!pip3 install date-extractor

#import geocoder
#from geopy import geocoders
#from geopy.geocoders import Nominatim
from geotext import GeoText
from date_extractor import extract_dates
import en_core_web_sm
#https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da

#url = 'http://www.bbc.com/news/world-europe-26919928'
#places = geograpy.get_place_context(url=url)

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
NER = en_core_web_sm.load()

############# Template 1 ##################
"""
Heuristic method
e.g. Words after lemmatized become [born, create, invent, ...] should be considered template 1
format: 
{
  "template": "BORN",
  "sentences": [ "Amazon was founded by Jeff Bezos in Bellevue, Washington, in July 1994."],
  "arguments": {
    "1": "Amazon",
    "2": "July 1994",
    "3": "Bellevue, Washington",
  }
}
"""

def initializeBornVerb():
  # bear
  wordList = ["created", "founded", "born", "constructed"]

  bornSet = set()
  
  for word in wordList:
    bornSet.add(word)    
    for synset in wn.synsets(word):
      for lemma in synset.lemmas():
        bornSet.add(lemma.name())
        #print(word, "has synonyms " ,lemma.name())

  return bornSet

def initializeMonthSet():
  monthSet = set()

  wordList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  
  for word in wordList:
    monthSet.add(word)    
    for synset in wn.synsets(word):
      for lemma in synset.lemmas():
        monthSet.add(lemma.name())
        #print(word, "has synonyms " ,lemma.name())
  return monthSet

def template1(sentence, words, bornSet, outputJson, nerDict):
  """
  sentence: raw string sentence
  words: lemmatized words + dependency parsing + POS tag
  bornSet: verbs related to born concepts
  outputJson: output for task 3
  nerDict: named entity dictionary ex: nerDict['GPE'] = set("Texas")
  
  Jeff NNP Bezos compound
  Bezos NNP founded nsubj
  founded VBD founded ROOT
  Amazon NNP founded dobj

  Amazon NNP founded nsubjpass
  was VBD founded auxpass
  founded VBN founded ROOT
  by IN founded agent
  Jeff NNP Bezos compound
  Bezos NNP by pobj
  in IN Bezos prep
  Bellevue NNP in pobj
  , , Bellevue punct
  Washington NNP Bellevue appos
  , , founded punct
  in IN founded prep
  July NNP in pobj
  1994 CD July nummod
  . . founded punct

  nsubj is the subject of the word. Its headword is a verb.
  aux is an auxiliary word. Its headword is a verb.
  dobj is the direct object of the verb. Its headword is a verb.
  """

  found = False
  rootVerb = ""
  for i in range(0, len(words)):
    if words[i].text == words[i].head.text:
      if words[i].text in bornSet and (words[i].tag_ == "VBN" or words[i].tag_ == "VBD"):
        print("BORN template was found!")
        found = True
        rootVerb = words[i].text
        break
    
    #print(words[i].text, words[i].tag_, words[i].head.text, words[i].dep_)

  if found is True:
    output = {}
    output["template"] = "BORN"
    output["sentences"] = words
    output["arguments"] = {}

    places = GeoText(sentence)
    #print(places.country_mentions)
    cities = set(places.cities)
    print("Cities mentioned:", cities)
    
    space = ""
    i = 0
    while i < len(words):
      
      if (words[i].dep == spacy.symbols.nsubjpass or words[i].dep == spacy.symbols.dobj) and words[i].head.text == rootVerb and words[i].tag_ == "NNP":
        output["arguments"]["1"] = words[i].text

      elif words[i-1].tag_ == "IN" and words[i].text in nerDict['GPE'] and words[i].text in cities:
        space += words[i].text
        link = words[i].text
        i += 1
        
        # add geotext.py
        while words[i].head.text == link:
          if words[i].dep == spacy.symbols.punct or words[i].text in nerDict['GPE']:
            space += words[i].text
            i += 1

        i -= 1

      i += 1
    
    if len(nerDict['DATE']) == 1:
      dateList = list(nerDict['DATE'])
      output["arguments"]["2"] = dateList[0]
    else:
      dates = extract_dates(text)
      #timestampStr = dates[0].strftime("%b %d %Y")
      timestampStr = dates[0].strftime("%H:%M:%S.%f - %b %d %Y")
      # '00:00:00.000000 - Jan 20 1994'
      output["arguments"]["2"] = timestampStr

    output["arguments"]["3"] = space

    outputJson["extraction"].append(output)
    return outputJson
  else:
    return

############# Template 2  ##################
"""
Heuristic method
e.g. Words after lemmatized become [buy, acquire, ...] should be considered template 2
ex: Amazon acquisitions include Ring, Twitch, Whole Foods Market, and IMDb in 2018.
try NER in argument 2
format: 
{
  "template": "BUY",
  "sentences": [ "In 2017, Amazon acquired Whole Foods Market for US$13.4 billion, which vastly increased Amazon's presence as a brick-and-mortar retailer."],
  "arguments": {
    "1": "Amazon",
    "2": "Whole Foods Market",
    "3": "2017",
  }
}
"""

def initializeBuyVerb():
  # bear
  wordList = ["buy", "acquire"]

  buySet = set()
  
  for word in wordList:
    buySet.add(word)    
    for synset in wn.synsets(word):
      for lemma in synset.lemmas():
        buySet.add(lemma.name())
        #print(word, "has synonyms " ,lemma.name())

  return buySet

def template2(sentence, words, buySet, outputJson, nerDict):
  """
  sentence: raw string sentence
  words: lemmatized words + dependency parsing + POS tag
  bornSet: verbs related to born concepts
  outputJson: output for task 3
  nerDict: named entity dictionary ex: nerDict['GPE'] = set("Texas")

  

  nsubj is the subject of the word. Its headword is a verb.
  aux is an auxiliary word. Its headword is a verb.
  dobj is the direct object of the verb. Its headword is a verb.
  """
  
  found = False
  rootVerb = ""
  for i in range(0, len(words)):
    if words[i].text == words[i].head.text:
      if words[i].text in buySet and (words[i].tag_ == "VBN" or words[i].tag_ == "VBD" or words[i].tag_ == "VB"):
        print("BUY template was found!")
        found = True
        rootVerb = words[i].text
        break
    
    print(words[i].text, words[i].tag_, words[i].head.text, words[i].dep_)
  
  if found is True:
    output = {}
    output["template"] = "BUY"
    output["sentences"] = words
    output["arguments"] = {}

    comp_1 = ""
    comp_2 = ""
    i = 0



    outputJson["extraction"].append(output)
    return outputJson
  else:
    return

############## Visualization and helper function for task 1 ###################

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_

"""
Put everything into lists + extract information method (task 1)
Test run (task 2 + task 3)

"""

##################  Loading corpus #########################
filename = "amazon.txt"
#inputs = open(filename, "r")
#text = inputs.read().decode('utf8')

text = "Amazon was founded by Jeff Bezos in Bellevue, Washington, in July 1994. "
#text += "Jeff Bezos founded Amazon in Bellevue, Washington, in July 1994. "
#text = "Jason was born in Richardson, Texas on Jan 20 1994. "
#text = "in Bellevue, Washington"
text += "In 2017, Amazon acquired Whole Foods Market for US$13.4 billion, which vastly increased Amazon's presence as a brick-and-mortar retailer."

##################  Load function for task 1  #################
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
lemmatizer = spacy.load('en_core_web_sm')
sentences = tokenizer.tokenize(text)

##################  Initialize verb set for template 1 and 2  ################
bornSet = initializeBornVerb()
buySet = initializeBuyVerb()
print("Born set:", bornSet)
print("Buy set:", buySet)

outputJson = {}
outputJson["document"] = filename
outputJson["extraction"] = []

###################  Main testing  ####################
for sentence in sentences:
  #### split, tokenize, lemmatize, pos, dependency parsing ####
  words = lemmatizer(sentence)
  tokens = []
  wordList = [token.orth_ for token in words]
  for word in words:
    tokens.append(word)

  pos_tags = nltk.pos_tag(wordList)  
  [to_nltk_tree(sent.root).pretty_print() for sent in words.sents]
  
  # Using WordNet, extract hypernymns, hyponyms, meronyms, AND holonyms as features
  """for word in wordList: 
    print("Word:"+word+"############################################")   
    for synset in wn.synsets(word):
      print(synset)
      print("Lemma:\n")
      for name in synset.lemma_names():
        print(name)
      print("hyper:\n")
      for hyper in synset.hypernyms():
        print(hyper)
      print("hypo:\n")
      for hypo in synset.hyponyms():
        print(hypo)
      print("holo:\n")
      for holo in synset.member_holonyms():
        print(holo)
      print("mero:\n")
      for mero in synset.member_meronyms():
        print(mero)
      print("part holo:\n")
      for holo in synset.part_holonyms():
        print(holo)
      print("sub holo:\n")
      for holo in synset.substance_holonyms():
        print(holo)
      print("part mero:\n")
      for mero in synset.part_meronyms():
        print(mero)
      print("sub mero:\n")
      for mero in synset.substance_meronyms():
        print(mero)"""
  
  #### named entity recognition ####
  named_entity = NER(sentence)
  #print([(X, X.ent_iob_, X.ent_type_) for X in named_entity])
  #print([(X.text, X.label_) for X in named_entity.ents])

  nerDict = {}
  for x in named_entity.ents:
    if x.label_ not in nerDict.keys():
      nerDict[x.label_] = set()
    nerDict[x.label_].add(x.text)
  print("Named Entity Set:", nerDict)

  #### matching templates ####
  template1(sentence, words, bornSet, outputJson, nerDict)
  template2(sentence, words, buySet, outputJson, nerDict)

  ########### Output for task 1  ##############
  """
  1. sentence
  2. tokenize the sentence
  3. Lemmatizd the words
  4. POS tag
  5. Dependency parsing
  6. hypernymns, hyponyms, meronyms, and holonyms
  7. Addition feature, ex: named entity recognition
  """
  #print(sentence)
  
  #for token in tokens:
    # print(token, " : ", token.lemma_, " : ", token.tag_)
  
  #print("POS tag by nltk:",pos_tags)
  
  #[to_nltk_tree(sent.root).pretty_print() for sent in words.sents]
  
  #
  
  #print([(ne.text, ne.label_) for ne in named_entity.ents])

print("Result::", outputJson)

#Template 3
place = GeoText("Amazon was founded by Jeff Bezos Richardson, Dallas, Texas, Houston, Katy, in, Bellevue, Washington, in July 1994. ")
print(place.cities)

"""# 新增區段

"""