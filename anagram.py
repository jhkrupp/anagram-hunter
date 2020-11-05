
#object we add in to first list of list to make comparisons more efficient for open addressing
class Word:
        def __init__(self, ordered, name):
            self.sorted = ordered
            self.regular = name

class Anagram(object):

    def __init__(self, filename):
        self.load_dictionary(filename)

    """
    Helper method to load the dictionary file.
    You may read it in some other way if you want to but do not change the function signature.
    """
    def load_dictionary(self, filename):
        with open(filename) as handle:
            self.dictionary = set(w.strip() for w in handle)

    """
    helper method for mergesort
    takes in a left and right list of letters
    returns a combined sorted list of left and right
    """
    def merge(self, left, right):
        sortedList = []
        leftIndex = 0
        rightIndex = 0
        leftLength = len(left)
        rightLength = len(right)
        for letter in range(rightLength + leftLength):
            #check to ensure we aren't going out of bounds
            if leftIndex < leftLength and rightIndex < rightLength:
                #seeing if the left side is alphabetically ahead of the right side and vice versa
                if ord(left[leftIndex]) <= ord(right[rightIndex]):
                    sortedList.append(left[leftIndex])
                    leftIndex += 1
                else:
                    sortedList.append(right[rightIndex])
                    rightIndex += 1
            #if one of the sides is empty just add the rest in
            elif rightIndex == rightLength:
                sortedList.append(left[leftIndex])
                leftIndex += 1
            elif leftIndex == leftLength:
                sortedList.append(right[rightIndex])
                rightIndex += 1
        return sortedList


    """
    We sort the word alphabetically using this function
    given a list of each letter in the word
    return a list of the sorted word
    """
    def mergesort(self, wordList):
        #base case
        if len(wordList) <= 1:
            return wordList
        #finds the middle then recurses down both sides
        mid = len(wordList) // 2
        left = self.mergesort(wordList[:mid])
        right = self.mergesort(wordList[mid:])
        #merges the 2 sides
        ansList = self.merge(left, right)
        return ansList

    '''
    Given a string word
    return a number unique to that word
    '''
    def myHash(self, word):
        num = 0
        index = 1
        for letter in word:
            num += (64**(len(word)-index)) * ord(letter)
            index += 1
        return num

    '''
    given a word, its sorted version, and the list of every word hashed in before it
    return the list but with the word in it
    basically just collision checking
    '''
    def hashIt(self, word, sortedWord, words):
        #getting us a key
        spot = self.myHash(sortedWord) % (len(words))
        #using an object to store both the word and its sorted versions to make future comparisons easier
        item = Word(sortedWord, word)
        index = spot
        while index < len(words):
            #checking if key spot in the list is empty
            if len(words[index]) == 0:
                #we can just put the object when there are no collisions
                words[index].append(item)
                break
            else:
                #check if the word in the key spot and the word we want to put in are anagrams of each other for collisions
                wordList = []
                key = words[index][0]
                if sortedWord == key.sorted:
                    words[index].append(item)
                    break
                #if they aren't then we just move to the next spot and check (open addressing)
                else:
                    index += 1
            #covering the wraparound
            if index >= len(words):
                index = 0
        return words    
        
    """   
   * Implement the algorithm here. Do not change the function signature.
   *
   * @returns - List of lists, where each element of the outer list is a list containing all the words in that anagram class.
   * example: [['pots', 'stop', 'tops'], ['brake', 'break']]
    """
    def getAnagrams(self):
        words = [[] for _ in range(5 * len(self.dictionary))]
        for x in self.dictionary:
            wordList = []
            key = x
            #turning string into list for mergesort to accept
            for element in key:
                wordList.append(element)
            alphabetize = "".join(self.mergesort(wordList))
            #need this because the first word is blank for some reason
            if len(x) != 0:
                words = self.hashIt(x, alphabetize, words)
        anagram = []
        #adding the anagram classes to this list to get rid of all the empty lists
        for stuff in words:
            if len(stuff) > 0:
                anagramList = []
                #pulling out the actual word from every object
                for item in stuff:
                    anagramList.append(item.regular)
                anagram.append(anagramList)
        return anagram

"""
You can use this for debugging if you wish.
"""
if __name__ == "__main__":
    pf = Anagram("dict1.txt")
    print(pf.getAnagrams())
    

