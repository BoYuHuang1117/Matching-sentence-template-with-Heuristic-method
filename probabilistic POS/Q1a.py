## NLP CS6320.003
## HW3 Q1a
## Name: Bo-Yu Huang
## NET ID: bxh190000

import sys

if len(sys.argv) != 2:
    print("Please type in the name of the corpus .txt as the first argument!!")
    exit()

filename = sys.argv[1]
l = len(filename)
if ".txt" != filename[l-4:l]:
    print("File type: ",filename[l-4:l])
    print("File type other than .txt file is not allowed!!")
    exit()
    
file = open(filename,"r")

uniWordSet = set()
uniWordCount = {}
uniTagSet = set()
uniTagCount = {}

wordTagSet = {}
biWTSet = set()
biWTCount = {}
biTTSet = set()
biTTCount = {}

uniTagSet.add("<s>")
uniTagCount["<s>"] = 0
uniTagSet.add("</s>")
uniTagCount["</s>"] = 0

# treat each line as separate sentence
# start of a sentecne <s>, end of a sentence </s>
for line in file:
    # Tokensize each word by " "
    # Separate POS tag and actual word by "_", ex: word_tag
    
    words_POS = line.split()
    words = [ word_POS.split("_")[0] for word_POS in words_POS]
    tags = [ word_POS.split("_")[1] for word_POS in words_POS]
    
    uniTagCount["<s>"] += 1
    uniTagCount["</s>"] += 1
    
    prevWord = words[0]
    prevTag = "<s>"
    
    if prevWord not in uniWordSet:
        wordTagSet[prevWord] = set()
        uniWordSet.add(prevWord)
        uniWordCount[prevWord] = 1
    else:
        uniWordCount[prevWord] += 1
    
    for i in range(1,len(words)):
        currWord = words[i]
        if currWord not in uniWordSet:
            wordTagSet[currWord] = set()
            uniWordSet.add(currWord)
            uniWordCount[currWord] = 1
        else:
            uniWordCount[currWord] += 1
        
        currTag = tags[i-1]
        if currTag not in uniTagSet:
            uniTagSet.add(currTag)
            uniTagCount[currTag] = 1
        else:
            uniTagCount[currTag] += 1
        
        wordTagSet[prevWord].add(currTag)    
        
        wordTag = prevWord + " " + currTag
        if wordTag not in biWTSet:
            biWTSet.add(wordTag)
            biWTCount[wordTag] = 1
        else:
            biWTCount[wordTag] += 1
        
        TT = prevTag + " " + currTag
        if TT not in biTTSet:
            biTTSet.add(TT)
            biTTCount[TT] = 1
        else:
            biTTCount[TT] += 1
        
        prevWord = currWord
        prevTag = currTag
    
    #### handling end of sentence case
    currTag = tags[-1]
    if currTag not in uniTagSet:
        uniTagSet.add(currTag)
        uniTagCount[currTag] = 1
    else:
        uniTagCount[currTag] += 1
    
    wordTagSet[prevWord].add(currTag)    
        
    wordTag = prevWord + " " + currTag
    if wordTag not in biWTSet:
        biWTSet.add(wordTag)
        biWTCount[wordTag] = 1
    else:
        biWTCount[wordTag] += 1    
    
    TT = prevTag + " " + currTag
    if TT not in biTTSet:
        biTTSet.add(TT)
        biTTCount[TT] = 1
    else:
        biTTCount[TT] += 1
    
    TT = currTag + " </s>" 
    if TT not in biTTSet:
        biTTSet.add(TT)
        biTTCount[TT] = 1
    else:
        biTTCount[TT] += 1
    
file.close()

###############################  Output  ###################################
"""
Calculate the unigram probability first (not necessary in this case)
"""
"""uniWordProb = {}
uniWordSum = sum(uniWordCount.values())
for item in uniWordCount.items():
    uniWordProb[item[0]] = item[1]/uniWordSum

uniTagProb = {}
uniTagSum = sum(uniTagCount.values())
for item in uniTagCount.items():
    uniTagProb[item[0]] = item[1]/uniTagSum
"""
###################################################
"""
Calculate the bigram probability for "No smoothing"
Output: biWTProb, biTTProb, biWTSet, biTTSet, wordTagSet
"""

biWTProb = {}
for item in biWTCount.items():
    tag = item[0].split()[1]
    biWTProb[item[0]] = item[1]/uniTagCount[tag]

biTTProb = {}
for item in biTTCount.items():
    prevTag = item[0].split()[0]
    biTTProb[item[0]] = item[1]/uniTagCount[prevTag]
    
# biWTProb
with open('biWTProb.txt', 'w') as f:
    for item in biWTProb.items():
        f.write("%s" % item[0]+" "+"%f\n" %item[1])

# biTTProb
with open('biTTProb.txt', 'w') as f:
    for item in biTTProb.items():
        f.write("%s" % item[0]+" "+"%f\n" %item[1])

# biWTSet
with open('biWTSet.txt', 'w') as f:
    for item in biWTSet:
        f.write("%s\n" % item)

# biTTSet
with open('biTTSet.txt', 'w') as f:
    for item in biTTSet:
        f.write("%s\n" % item)
        
# wordTagSet
with open('wordTagSet.txt', 'w') as f:
    for item in wordTagSet.items():
        f.write("%s" % item[0] + ":")
        for tag in item[1]:
            f.write(" "+"%s" % tag)
        f.write("\n")