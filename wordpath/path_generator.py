import string
import model
## This method receives a beginning word and an end word and go through a given list of words searching for paths between the beginning one and the end one, returning a list of possibles paths
## To search in the list it bases on the algorithm for searching in graphs Breadth-first search
##undestanding that there is a connection between each vertice(word) that has no more that one letter of difference
def generateWordPaths(beginWord, endWord, wordList):
    queue = []
    firstPath = model.WordPath([beginWord])
    queue.append(firstPath)
    visited = set(beginWord)
    generatedPaths = []
    while queue:

        path = queue.pop(0)

        lastWord = path.lastWord()
        sameLevel = False
        connectedWords = getConnectedWord(lastWord, wordList)
        if(path.lastWord() == 'cat'):
            print(connectedWords)
            print(path.getPath())
        ## First it checks whether this word has already a connection with the end word, in case yes I generate a path and go for the next
        if(endWord in connectedWords):
            path.addNewWord(endWord)
            generatedPaths.append(path)
            continue
        for connectedWord in connectedWords:

            ## if the word was already visited it will jump to the next iteration
            if(connectedWord in visited):
                continue
            if(connectedWord == 'cad'):
                print(connectedWord)
                print(path.getPath())
            ## if it is in the same level, means that this is a sibling of the last visited node so a new path has been generated
            if(sameLevel):
                newPath = model.WordPath(path.getParentPath())
                newPath.addNewWord(connectedWord)
                visited.add(connectedWord)
                queue.append(newPath)

            else:  # if it is not in the same level, means that it will be added to the current path as at the moment is not need to create another path
                path.addNewWord(connectedWord)
                visited.add(connectedWord)
                queue.append(path)
                sameLevel = True

    return generatedPaths

## This method receives a word and a list of word, generate all possibilities of siblings(every word that has only one letter different) and check if it is in the list of words, siblings are consider connected
def getConnectedWord(word, wordList):
    connectedWords = []
    for i in range(len(word)):
        for letter in string.ascii_letters:
            connected = word[:i] + letter + word[i+1:]
            if connected in wordList:
                connectedWords.append(connected)
    return connectedWords
