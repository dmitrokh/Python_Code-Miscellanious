import random
import os

kVowels = 'aeiou'
kConsonants = 'bcdfghjklmnpqrstvwxyz'
kDealSize = 7
kMaxHand = 12

kLetterValues = {
   'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 
   'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 
   's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

kWordsFilename = "words.txt"

def loadWords():
   wordList = []
   i = 0
   file = open('.\\words.txt', 'r')
   for line in file:
      line = line.strip()
      line = line.lower()
      wordList.append(line)
      i += 1
   print("loading words from file... \n", i, "words loaded")
   return wordList

def buildUseDict(word):
    wordDict = dict()
    for char in word:
       wordDict[char] = wordDict.get(char, 0) + 1
    return wordDict

def testBuildUseDict():
   passed = True
   testCases = ['','a','ab','aba']
   expectRes = [{},{'a':1},{'a':1,'b':1},{'a':2,'b':1}]
   for i,t in enumerate(testCases):
       if expectRes[i] != buildUseDict(t):
           print("Failed on testCase: ", t)
           passed = False
   if not passed:
      print("testBuildUseDict... failed")
   return passed

def scoreWord(word, n):
    score = 0
    if len(word) == n:
        score += 50
    for char in word:
        score += kLetterValues.get(char, 0)
    return score

def testScoreWord():
   passed = True
   testCases = [('',1),('a',2),('a',1),('xyz',5)]
   expectRes = [0,kLetterValues['a'],50+kLetterValues['a'],kLetterValues['x']+kLetterValues['y']+kLetterValues['z']]
   for i,t in enumerate(testCases):
       if expectRes[i] != scoreWord(t[0],t[1]):
           print("Failed on testCase:  ", t)
           passed = False
   if not passed:
      print("testScoreWord...failed")
   return passed       
                
def showHand(hand):
    strRes = ''
    for key in hand:
        if hand.get(key) == 1: 
            strRes += key
        else:
            strRes += key * hand.get(key, 0)
    return ' '.join(strRes)

def testShowHand():
   print("testShowHand... check visually:")
   testCases = [{},{'a':3},{'a':1,'b':2,'c':1,'d':3}]
   for i in range(len(testCases)):
      print("testCase:", testCases[i], ", showHand output:", showHand(testCases[i]))
   
def dealHand(hand, n):
   n = int(n)
   nVowels = n // 3 + (random.random() <  (n % 3) * .33334)
   for i in range(0, nVowels):
      chari = random.randrange(0,len(kVowels))
      if kVowels[chari] not in hand:
            hand[kVowels[chari]] = 1
      else:
            hand[kVowels[chari]] += 1
   nCons = n - nVowels
   for i in range(0, nCons):
      chari = random.randrange(0,len(kConsonants))
      if kConsonants[chari] not in hand:
            hand[kConsonants[chari]] = 1
      else:
            hand[kConsonants[chari]] += 1
   return hand

def testDealHand():
   passed = True
   d = dealHand({}, 0)
   if countValues(d) != 0 or countVowels(d) != 0:
      print("failed on input ({}, 0)")
      passed = False
   d = dealHand({}, 3)
   if countValues(d) != 3 or countVowels(d) < 1:
      print("failed on input ({}, 3)")
      passed = False
   d = dealHand({'a':3}, 7)
   if countValues(d) != 10 or countVowels(d) < 3:
      print("failed on input ({'a':3}, 7)")
      passed = False
   if not passed:
      print("testDealHand...failed")
   return passed

def countValues(hand):
   return sum(hand.values())

def countVowels(hand):
   vowels = 0
   for key in hand:
      if key in kVowels:
         vowels += hand.get(key)
   return vowels
    
def removeWordFromHand(hand, word):
    for letter in word:
        if hand.get(letter) == 1:
            del(hand[letter])
        else:
            hand[letter] = hand.get(letter, 0) - 1
    return hand

def testRemoveWordFromHand():
   passed = True
   testCases = [({},''),({'a':1}, 'a'),({'a':2}, 'a'),({'a':1, 'b':2}, 'ab')]
   expectRes = [{}, {}, {'a':1}, {'b':1}]
   for i,t in enumerate(testCases):
       if expectRes[i] != removeWordFromHand(t[0],t[1]):
           print("failed")
           passed = False
   if not passed:
      print("testRemoveWordFromHand...failed")
   return passed

def isValid(word, hand, wordList):
   valid = True
   wordDict = dict()
   if len(word) != 0:
       for char in word:
          wordDict[char] = wordDict.get(char, 0) + 1
   if len(wordDict) != 0:
       for key in wordDict:
           if key not in hand or wordDict.get(key) > hand.get(key):
               valid = False
   if word not in wordList: valid = False
   return valid

def testIsValid():
   passed = True
   #testCases = [('', {}, wordList),('', {'a':2}, []),('a', {'a':1}, []),('aa', {'a':1}, []), ('aab', {'a':3,'b':1}, []),('aabb', {'a':3,'b':1}, [])]
   testCases = [('good', {'g':1,'o':2,'d':1}, wordList), ('goood', {'g':1,'o':2,'d':1}, wordList), ('bugaga', {'b':1,'g':2,'a':2,'u':1}, wordList), ('buugaga', {'b':1,'g':2,'a':2,'u':1}, wordList)]
   #expectRes = [True, True, True, False, True, False]
   expectRes = [True, False, False, False]
   for i,t in enumerate(testCases):
       if expectRes[i] != isValid(t[0],t[1],t[2]):
          passed = False
       #print(t[0],t[1], isValid(t[0],t[1],t[2]))
   if not passed:
      print("testIsValid...failed")
   return passed
            
def playRound(hand, wordList):
   roundTotal = 0
   word = ''
   while len(hand) and word != '.':
      print(showHand(hand))
      word = input("Enter word built from hand or . to end round: ")
      while isValid(word, hand, wordList) != True and word != '.':
         word = input("Invalid word, try again: ")
      if word == '.':
         #hand = {}
         break
      n = countValues(hand)
      score = scoreWord(word, n)
      print(word, ":", score, "pts")
      removeWordFromHand(hand, word)
      showHand(hand)
      roundTotal += score
      if not len(hand):
         print('playRound not implemented')
   print("Round score = ", roundTotal, end ='')
   return roundTotal
 
def playGame(wordList):
   hand = {}
   scoreTotal = 0
   kMaxHand = input("Enter maximum number of letters in hand: ")
   while kMaxHand.isdigit() != True:
        kMaxHand = input("Enter maximum number of letters in hand (An integer number): ")
   choice = input("Enter 'n' to start a new round, 'l' to load saved game or 'e' to end game: ")
   while choice != 'e':
      if choice == 'l' or choice == 'L':
         file = open(".\\wordRummyState.txt", 'r')
         file.seek(0)
         scoreTotal = int(file.readline())
         for line in file:
            key = line.split(':')[0]
            hand[key] = int(line.split(':')[1])
         file.seek(0)
         file.close()
         dealHand(hand, kMaxHand)
         scoreTotal += playRound(hand, wordList)
         print(" Total score: ", scoreTotal)
      elif choice == 'n' or choice == 'N':
         dealHand(hand, kMaxHand)
         scoreTotal += playRound(hand, wordList)
         print(" Total score: ", scoreTotal)
      elif choice == 's' or choice == 'S':
         file = open('.\\wordRummyState.txt', 'w')
         into = str(scoreTotal)+'\n'
         file.write(into)
         for key in hand:
            into = str(key)+":"+str(hand[key])+'\n'
            file.write(into)
         file.close()
      else:
         print("Invalid command")
      print('playGame not implemented')
      choice = input("Enter command? 'e' - end game, 's' - save score, 'l' - load saved hand, 'n' - new round: ")
     
if __name__ == '__main__':
    wordList = loadWords()
    testBuildUseDict()
    testScoreWord()
    #testShowHand()
    testDealHand()
    testRemoveWordFromHand()
    testIsValid()
    playGame(wordList)
    
