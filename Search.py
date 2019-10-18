import os
import errno

FILE_NAME_LENGTH = 30
COUNT_NAME_LENGTH = 4
POINTER_LENGTH = 50

def main():
    # read from console the keyword search
    print('WORD SEARCH 0.1')
    directoryString = input('Dir: ')
    if not os.path.exists(directoryString):
        print("must be a working directory\n")
        main()
    searchString = input('Search: ')
    search(directoryString, searchString.lower())

def search(directoryString, searchStr):
    foundBool = False
    # search and output
    os.chdir(directoryString)
    for file in os.listdir(directoryString):
        if os.path.isfile(file):
            try:
                with open(file, errors='ignore') as fileinput:
                    for count, line in enumerate(fileinput):
                        lineStr = line.lower()
                        pointer = '^'
                        if searchStr in lineStr:
                            foundBool = True
                            set = StringSet(searchStr, os.path.basename(file), count, line, pointer)
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
    if (len(set.pointer) > POINTER_LENGTH):
        print(set.pointer)

# boxes up the strings
class StringSet:
    def __init__(self, searchStr, basename, count, line, pointer):
        self.searchStr = searchStr
        self.basename = basename
        self.count = count
        self.line = line
        self.pointer = pointer

main()
