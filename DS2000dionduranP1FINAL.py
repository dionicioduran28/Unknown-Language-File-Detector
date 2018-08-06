import sys
import string 
import math 
from operator import itemgetter



#takes in input file and returns two dictionaries with each language as key and 
#list of text files as values for each language
def readInputFile(filename):
    langDict = {}
    unknownDict = {}
    file = open(filename)
    
    #iterate through each line of input file 
    for line in file:
        #split line so that lang or unk is in 1st postion and filename in 2nd
        split = line.split()
        
        #if language is unknown create dictionary where filename is both key 
        #and value 
        if split[0] == 'Unknown' and split [1] not in unknownDict:
            unknownDict[split[1]]= []    
        if split[0] == 'Unknown' and split [1] in unknownDict:
            unknownDict[split[1]].append(split[1])
        
        #if language is known add that language to known dictionary 
        #where the key is the language and the value is list of filenames 
        if split[0] not in langDict and split[0] != 'Unknown':
            langDict[split[0]] = []
        if split[0] in langDict and split[0] != 'Unknown':
            langDict[split[0]].append(split[1])
    
    return langDict,unknownDict


def readTextDict(langDict):
    badList = ['0','1','2','3','4','5','6','7','8','9', '-','\n']

    updateDict = {}

    #iterate through known dictionaries and return dictionary which contains 
    #language as key and all words for that lanaguae read in from files    
    for i in langDict:
        updateDict[i] = []
        for j in langDict[i]:
            file = open(j, encoding='utf-8')
            for line in file:
                sentence = line.rstrip().lower()
                updateDict[i].append(sentence)
                         
    #iterate through dictionary of dictionaries 
    # with languages as keys and updates that dictionary so 
    #it now contains clean data as a list with each char as element 
    for i in updateDict:
        charList = []
        for j in updateDict[i]:
            for k in j:
                if k not in string.punctuation and k not in badList:
                    charList.append(k)
        updateDict.update({i:charList})
    return updateDict

#function takes in dictionary were keys are language or unk textfile name 
#and valus are a list of each character cleaned 
def createTrigramDict(updateDict):
    triDict = {}
    triLenDict = {}
  
    #create two new dictionaries, one where it holds the trigrams as keyys and 
    #one that holds the number of trigrams in each one, iterate through update dict
    #to create them
    for i in updateDict:
        triDict[i] = []
        triLenDict[i] = []
        triList = []
        for j in range(len(updateDict[i])-2):

            triList.append(updateDict[i][j]+updateDict[i][j+1]+updateDict[i][j+2])
            
        triDict.update({i:triList})
        triLenDict.update({i:len(triList)})
     
    
    #update triDict so that it now holds dictionaries with the freqeuenies of each 
    #trigram 
    for i in triDict:
        specLangDict = {}
        for j in triDict[i]:
            if j not in specLangDict:
                specLangDict[j] = 1
            if j in specLangDict:
                specLangDict[j] += 1 
        triDict.update({i:specLangDict})
            
    #iterate through tridict and triLenDict simultaneously to update values
    #with normalzied percentages 
    for i in triDict:
        for j in triLenDict:
            if i == j:
                for k in triDict[i]:
                    x = triDict[i][k]/triLenDict[j]
                    triDict[i].update({k:x})
                   
    return triDict

#function will take in known and unk dictionaries and return a single dictionary
#where the key is 'language,filename' and the value is 0 '
def createLangFileDict(lanDict,unkDict):
    langFileDict = {}
    
    #iterare through unkDict and lanDict and create a new dictionary where 
    #the key is 'filename,language' and value 0
    for i in unkDict:
        for j in lanDict:
            langFileDict[i,j] = 0
    return langFileDict

#update langFileDict so that key:filename,language value: angle by finding 
#intersection points between each known languuage dict and each unknown file
def findIntersects(unkDict,lanDict,langFileDict):
   
   
   #iterate through both unknown and known dictionaries finding the intersection 
    #of the two where the trigrams(key) mathch 
    for i in unkDict:
        iSet = set(unkDict[i].keys())
        for j in lanDict:
            jSet = set(lanDict[j].keys())
            
            sumAiSqed = 0
            sumBiSqed = 0
            sumAixBi = 0 
            #cosine caculations done below performing the following equations 
            #at each intersection of trigrams 
            for k in iSet&jSet:
                sumAixBi += unkDict[i][k] * lanDict[j][k]
                sumAiSqed += unkDict[i][k]**2
                sumBiSqed += lanDict[j][k]**2
            coSine = sumAixBi/(math.sqrt(sumAiSqed)*math.sqrt(sumBiSqed))
            langFileDict[i,j] += coSine
           
    return langFileDict

#takes in dictionary which contains all cosine value and returns a new dict 
#sorted firt by text file and then by value 
def sortDict(langFileDict):
    sort = sorted(langFileDict.items(), key = itemgetter(0), reverse = True)
    sortedDict = {}

    for i in sort:
        if i[0][0] not in sortedDict:
            sortedDict[i[0][0]] = []
        if i[0][0] in sortedDict:
            sortedDict[i[0][0]].append((i[0][1],i[1]))

    for i in sortedDict:
        sortedDict[i].sort(key = itemgetter(1), reverse = True)

    return sortedDict     

#function takes in sorted dictionary and writes to output 
def storeResults(filename, sortedDict):
    file = open(filename, 'w')
    for i in sortedDict:
        file.write(str(i) + '\n')
        for j in sortedDict[i]:
            file.write(str(j) + '\n')
            
    file.close()

def main():
    
    readInput = readInputFile('languagescopy.txt')
    langList = readTextDict(readInput[0])
    unkList = readTextDict(readInput[1])
    
    
    lanDict = createTrigramDict(langList)
    unkDict = createTrigramDict(unkList)
    
    LangFileDict = createLangFileDict(lanDict,unkDict)
    
    intersect = findIntersects(unkDict,lanDict,LangFileDict)
    
    sortedDict = sortDict(intersect)
    writeResults = storeResults('results.txt', sortedDict)


main()