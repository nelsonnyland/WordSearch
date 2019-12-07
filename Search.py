import os
import errno
import glob
import sys
import pathlib

FILE_NAME_LENGTH = 30
COUNT_NAME_LENGTH = 4
POINTER_LENGTH = 55

def main():
    intro()
    # read from console
    path = input('Dir: ')
    # validate dir
    dirValidate(path)
    # receive search term
    words = input('Search: ')
    # test search mode
    mode = testMode(words)
    # begin operation
    openDir(path, words, mode)
    # restart
    main()

# prints intro text
def intro():
    print('WORD SEARCH 0.1')
    print('Searches TXT files within given directory and subdirectories. ' + 
          'Use quotes to clarify search term.')
    print('Enter \'q\' to exit.')

# validates directory
def dirValidate(path):
    # check for exit command
    if path.lower() == 'q':
        sys.exit()
    # correct backslashes
    path.replace('\\', '/')
    # check if directory exists
    if not os.path.exists(path):
        print("must be a working directory\n")
        main()

# returns search mode: 1 for literal, 0 for default
def testMode(s):
    if ((s.startswith('\'') and s.endswith('\'')) or
        (s.startswith('\"') and s.endswith('\"'))):
        return 1
    else:
        return 0

# opens and searches files
def openDir(path, words, mode):
    foundBool = False
    # search and output
    os.chdir(path)
    for file in glob.iglob(path + '/**/*.txt', recursive=True):
        if os.path.isfile(file):
            try:
                with open(file, errors='ignore') as fileinput:
                    for count, line in enumerate(fileinput):
                        set = StringSet(mode, words, file, count, line)
                        if search(set):
                            foundBool = True
                            printToConsole(formatStrings(set))
            except IOError as e:
                if e.errno == errno.ENOENT:
                    print(os.path(file), ' does not exist')
                if e.errno == errno.EACCES:
                    print(os.path(file), ' cannot be read')
                else:
                    print(os.path(file), e)
    if foundBool is False:
        print('**NO WORDS FOUND**')

def search(set):
    if set.mode == 0:
        if set.words in set.line:
            return True
    elif set.mode == 1:
        set.words = set.words.strip('\"')
        set.words = set.words.strip('\'')
        newSearch = ' ' + set.words + ' '
        if newSearch in set.line:
            return True

# processes the strings to format in console
def formatStrings(set):    
    if len(set.path) > FILE_NAME_LENGTH:
        set.path = '...' + set.path[len(set.path) - 
                    FILE_NAME_LENGTH:len(set.path)] + ' - '
    set.count += 1
    set.count = str(set.count) + ':'
    if len(set.count) > COUNT_NAME_LENGTH:
        set.count = set.count.rstrip(':')
        set.count = set.count[0:COUNT_NAME_LENGTH - 1] + '~'
    else:
        set.count = set.count.ljust(COUNT_NAME_LENGTH)
    set.line = set.line.rstrip('\n')    
    index = set.line.find(set.words)    
    set.pointer = set.pointer.rjust(index + POINTER_LENGTH)
    return set

# print to console
def printToConsole(set):
    print('FILE: {} LINE {} \"{}\"'.format(set.path, set.count, set.line))
    if len(set.pointer) > POINTER_LENGTH:
        print(set.pointer)

# boxes up the strings
class StringSet:
    def __init__(self, mode, words, path, count, line):
        self.mode = mode
        self.words = words
        self.path = path
        self.count = count
        self.line = line.lower()
        self.pointer = '^'

main()
