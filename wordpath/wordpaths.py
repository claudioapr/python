import constant
import path_generator as PathGenerator
import model
import sys
# This file aim to keep the interation with the user
def main():
    inputArray = []
    if(len(sys.argv) > 3):
        inputArray = sys.argv[1:4]
    else :
        inputArray = readInput().split(" ")

    numOfTry = 0;
    # This "while" aims to check whether the number of the input is right or not, and give another chance
    while (len(inputArray) != 3):
    #But to not end up in a loop, a limit is stipulated, therefore if the user reaches this limit the system is ended and the user has to run the script again
            if numOfTry > constant.INPUT_NUM_MAX_TRY:
                print("Number max of try reached... ending the script")
                #to avoid import sys exit using quit
                quit()

            print("Wrong number of arguments please try again")
            inputArray = readInput().split(" ");
            numOfTry += 1;

    filePath = inputArray[0]
    beginWord = inputArray[1]
    endWord = inputArray[2]
    # Begin words must have the same number of the letter that end words otherwise no path is available
    if len(beginWord) != len(endWord):
        print(constant.NO_PATH_AVAILABLE % (beginWord, endWord))
        quit()

    wordSize = len(beginWord);
    filteredWords = readWordsFromFileFilteringBySize(filePath, wordSize)

    paths = PathGenerator.generateWordPaths(beginWord, endWord, filteredWords)
    if len(paths) == 0:
        print(constant.NO_PATH_AVAILABLE % (beginWord, endWord))
        quit()

    for path in paths:
        printerFormmated(path)

def readInput():
    return input("Type the PATH for the file of the dictionary, BEGING word and the END word sparated by SPACE(e.g /user/share/dict/word cat dog). ->: ")

# To avoid overload, read line by line, instead of loading everything, also is filtered
def readWordsFromFileFilteringBySize(filePath, size):
    filteredWords = set()
    file = open(filePath, "r")
    with file:
        for line in file:
         normalizedLine = line.strip()
         if len(normalizedLine) == size:
            filteredWords.add(normalizedLine)
    return filteredWords
def printerFormmated(path):
    outPut = ""
    for word in path.getPath():
        outPut = outPut + word + constant.OUTPUT_WORD_DIVIDER
    print(outPut[:-2])

if __name__== "__main__":
  main()
