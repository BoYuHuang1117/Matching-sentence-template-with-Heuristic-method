## NLP CS6320.003
## HW3 Q1b
## Name: Bo-Yu Huang
## NET ID: bxh190000

############################## Input Sentence ################################
testing = input("Type your testing sentence\n") 

if testing == "":
    print("Testing string is empty!")
    exit()

############################## load files ###############################

biWTProb = {}
file = open("biWTProb.txt", "r")

for line in file:
    tokens = line.split()
    biWTProb[tokens[0]+" "+tokens[1]] = float(tokens[2])

file.close()

biTTProb = {}
file = open("biTTProb.txt","r")

for line in file:
    tokens = line.split()
    biTTProb[tokens[0]+" "+tokens[1]] = float(tokens[2])

file.close()

wordTagSet = {}
file = open("wordTagSet.txt", "r")

for line in file:
    tokens = line.split(":")
    wordTagSet[tokens[0]] = set(tokens[1].split())

file.close()

biWTSet = set()
file = open("biWTSet.txt","r")

for line in file:
    tokens = line.split()
    biWTSet.add(tokens[0]+" "+tokens[1])

file.close()

biTTSet = set()
file = open("biTTSet.txt","r")

for line in file:
    tokens = line.split()
    biTTSet.add(tokens[0]+" "+tokens[1])

file.close()

#############################  Output  ############################

def POSPredict(biWTProb, biTTProb, wordTagSet, biWTSet, biTTSet, testing):
    # calculate probability
    testTokens = testing.split()

    tagList = []    
    for word in testTokens:
        if word not in wordTagSet.keys():
            print("The word '", word, "' is not in the corpus,", "so..... 0 probability!")
            return
        
        tags = list(wordTagSet[word])
        tagList.append(tags)

    tagSeqs = [tagList[0]]

    for i in range(1,len(tagList)):
        L = len(tagSeqs)
        l = len(tagList[i])
        
        for j in range(0,l):
            for k in range(0,L):
                if j != l-1:
                    oldList = tagSeqs[k+L*j].copy()
                    tagSeqs.append(oldList)
                tagSeqs[k+L*j].append(tagList[i][j])
        #print(tagSeqs)

    # [tag1 tag2 tag3] => p(word1|tag1)*p(tag1|<s>)*p(word2|tag2)*p(tag2|tag1)*p(word3|tag3)*p(tag3|tag2)*p(</s>|tag3)
    prob = []
    for poss in tagSeqs:
        print("###########################")
        print("Compute Tag sequence....", poss)
        
        # tag given tag
        currProb = 1
        prevTag = "<s>"
        for i in range(0,len(poss)):
            currTag = poss[i]
            TT = prevTag+" "+currTag
            
            if TT not in biTTSet:
                print("Probability of '",TT,"' is 0")
                currProb = 0
                break
            else:
                print("Probability of '", TT, "' is", biTTProb[TT])
                currProb *= biTTProb[TT]
            
            prevTag = currTag
        
        TT = prevTag+" "+"</s>"   
        if TT not in biTTSet:
            print("Probability of '",TT,"' is 0")
            currProb = 0
        else:
            print("Probability of '", TT, "' is", biTTProb[TT])
            currProb *= biTTProb[TT] 
            
        if currProb == 0:
            prob.append(0)
            continue
            
        # word given tag
        for i in range(0,len(poss)):
            tag = poss[i]
            word = testTokens[i]
            
            WT = word+" "+tag
            
            if WT not in biWTSet:
                print("Probability of '",WT,"' is 0")
                currProb = 0
                break
            else:
                print("Probability of '", WT, "' is", biWTProb[WT])
                currProb *= biWTProb[WT]
        
        print("Probability:",currProb,"\n")
        prob.append(currProb)
        
    maxProb = max(prob)
    idx = [i for i, value in enumerate(prob) if value == maxProb]

    for i in idx:
        print("Max Probability:",maxProb)
        print("The max probability of POS sequence according to your input sentence is", tagSeqs[i])

POSPredict(biWTProb, biTTProb, wordTagSet, biWTSet, biTTSet, testing)

