## NLP CS6320.003
## HW3 Q2
## Name: Bo-Yu Huang
## NET ID: bxh190000

transProb = {}

uniTag = ["<s>", "NNP", "MD", "VB", "JJ", "NN", "RB", "DT"]
file = open("q2TransProb.txt", "r")

i = 0
for line in file:
    tokens = line.split()
    
    for j in range(0,len(tokens)):
        transProb[uniTag[i]+" "+uniTag[j+1]] = float(tokens[j])
    
    i += 1

file.close()

wordTagSet = {}
observLikeli = {}

file = open("q2Observ.txt", "r")

for line in file:
    tokens = line.split()
    if tokens[0] not in wordTagSet.keys():
        wordTagSet[tokens[0]] = set()
    
    wordTagSet[tokens[0]].add(tokens[1])
    observLikeli[tokens[0]+" "+tokens[1]] = float(tokens[2])

file.close()

#print(transProb)
#print(observLikeli)

################################ Viterbi algorithm ###############################
"""
Compute most likely tag sequence and its probability

i. Janet will back the bill
ii. will Janet back the bill
iii. back the bill Janet will
"""
def viterbiAlgo(transProb, observLikeli, wordTagSet, testing):
    testTokens = testing.split()
    currProbs = []
    currProbs.append({})
    
    for tag in wordTagSet[testTokens[0]]:
        key = "<s>"+" "+tag
        currProbs[0][key] = transProb[key]*observLikeli[testTokens[0]+" "+tag]
    
    for i in range(1,len(testTokens)):
        currProbs.append({})
        
        for newTag in wordTagSet[testTokens[i]]:
            key = " "+newTag
            stateMax = 0
            
            for item in currProbs[i-1].items():
                currTag = item[0].split()[-1]
                stateCurrProb = item[1]*transProb[currTag+" "+newTag]*observLikeli[testTokens[i]+" "+newTag]
                
                if stateCurrProb > stateMax:
                    key = item[0]+" "+newTag
                    stateMax = stateCurrProb
                
            currProbs[i][key] = stateMax
            
    
    print(currProbs)
    print("\n")
    
    tagSeq = ""
    value = 0
    for idx, v in currProbs[len(testTokens)-1].items():
        if v > value:
            tagSeq = idx
            value = v
            
    return tagSeq, value
    
    
## Sentence one ##
sent1 = "Janet will back the bill"
tagSeq1, prob1 = viterbiAlgo(transProb, observLikeli, wordTagSet, sent1)

print("The tag sequence with max probability of '", sent1, "' :", tagSeq1, "\nProbability:",prob1)
print("\n")

## Sentence two ##
sent2 = "will Janet back the bill"
tagSeq2, prob2 = viterbiAlgo(transProb, observLikeli, wordTagSet, sent2)

print("The tag sequence with max probability of '", sent2, "' :", tagSeq2, "\nProbability:",prob2)
print("\n")

## Sentence three ##
sent3 = "back the bill Janet will"
tagSeq3, prob3 = viterbiAlgo(transProb, observLikeli, wordTagSet, sent3)

print("The tag sequence with max probability of '", sent3, "' :", tagSeq3, "\nProbability:",prob3)