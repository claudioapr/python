import copy
## This class store the main information for a Path of a word
## Stores the last word add in the path, the source of this path(the root path that originated the instance)
## and the word path itself
class WordPath:
    def __init__(self, initPath):
        self.path = initPath
        self.lastElement = self.path[-1]

    def addNewWord(self, newWord):
        self.lastElement = newWord
        self.parentPath = copy.deepcopy(self.path)
        self.path.append(newWord)

    def lastWord(self):
        return self.lastElement

    def getPath(self):
        return self.path

    def getParentPath(self):
        return copy.deepcopy(self.parentPath)
