# Word Paths by Claudio Resende

The goal of this python script is implement the solution for the proposed problem Word Paths

The description of the problem is:
"The program should take as input the path to the word file, any start word and an end word and
print out at least one path from start to end, or something indicating there is no possible path if
appropriate. e.g.
$ python ./wordpaths.py /usr/share/dict/words cat dog
cat > cag > cog > dog "

## Enclosed files
 files below they are listed
 
  * words - File got from a Linux Mint 18 machine to perform tests and support in the development
  * wordpaths.py - This is the entry point of the script, where the user interaction is performed
  * constant.py - This is a file with some constants for the script, as is quite little is not so useful, but here we go.
  * model.py - This is the module where the models are in that case only one class WordPath
  * path_generator.py - This is the brain, where is created the paths for the words

### Python Version
  Python 3.7.4
## Presumptions

* Begin words must have the same number of the letter that end words otherwise no path is available will be displayed

### How to run
  To run the script we have 2 options passing the args trough the system args for the script, or executing the script and interacting with it, below some command samples.
  In those case the script was run inside of the root folder
  * Tested Linux and Windows 10 with the proper python configuration
  - $ python ./wordpaths.py words cat dog
  - $ python ./wordpaths.py
      $ Type the PATH for the file of the dictionary, BEGING word and the END word separated by SPACE(e.g /user/share/dict/word cat dog). ->: words cat dog


## Authors

**Claudio Resende**
