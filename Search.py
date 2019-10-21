import os
import errno

FILE_NAME_LENGTH = 30
COUNT_NAME_LENGTH = 4
POINTER_LENGTH = 50

def main():
    # read from console
    print('WORD SEARCH 0.1')
    directoryString = input('Dir: ')
    if not os.path.exists(directoryString):
        print("must be a working directory\n")
        main()
    searchStr = input('Search: ')
    mode = testMode(searchStr)
    openDir(directoryString, searchStr, mode)

# returns search mode: 1 for literal, 0 for default
def testMode(s):
    if ((s.startswith('\'') and s.endswith('\'')) or
        (s.startswith('\"') and s.endswith('\"'))):
        return 1
    else:
        return 0

# opens and searches files
def openDir(directoryString, searchStr, mode):
    foundBool = False
    # search and output
    os.chdir(directoryString)
    for file in os.listdir(directoryString):
        if os.path.isfile(file):
            try:
                with open(file, errors='ignore') as fileinput:
                    for count, line in enumerate(fileinput):
                        set = StringSet(mode, searchStr, os.path.basename(file), count, line)
                        if search(set):
                            foundBool = True
                            printToConsole(processStrings(set))
            except IOError as e:
                if e.errno == errno.ENOENT:
                    print(os.path.basename(file), ' does not exist')
                if e.errno == errno.EACCES:
                    print(os.path.basename(file), ' cannot be read')
                else:
                    print(os.path.basename(file), e)
    if foundBool is False:
        print('**NO WORDS FOUND**')

def search(set):
    if set.mode is 0:
        if set.searchStr in set.line:
            return True
    elif set.mode is 1:
        set.searchStr = set.searchStr.strip('\"')
        set.searchStr = set.searchStr.strip('\'')
        newSearchStr = ' ' + set.searchStr + ' '
        if newSearchStr in set.line:
            return True

# processes the strings to format in console
def processStrings(set):
    if len(set.basename) > FILE_NAME_LENGTH:
        set.basename = set.basename[0:FILE_NAME_LENGTH - 3] + '...'
    else:
        set.basename = set.basename.ljust(FILE_NAME_LENGTH)
    set.count += 1
    set.count = str(set.count)
    if len(set.count) > COUNT_NAME_LENGTH:
        set.count = set.count[0:COUNT_NAME_LENGTH - 1] + '~'
    else:
        set.count = set.count.ljust(COUNT_NAME_LENGTH)
    set.line = set.line.rstrip('\n')    
    index = set.line.find(set.searchStr)    
    set.pointer = set.pointer.rjust(index + POINTER_LENGTH)
    return set

# print to console
def printToConsole(set):
    print('FILE: {} LINE {}: \"{}\"'.format(set.basename, set.count, set.line))
    if len(set.pointer) > POINTER_LENGTH:
        print(set.pointer)

# boxes up the strings
class StringSet:
    def __init__(self, mode, searchStr, basename, count, line):
        self.mode = mode
        self.searchStr = searchStr
        self.basename = basename
        self.count = count
        self.line = line.lower()
        self.pointer = '^'

main()
