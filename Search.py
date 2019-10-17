import os
import errno

def main():
    # read from console the keyword search
    print('WORD SEARCH 0.1')
    directoryString = input('Dir: ')
    if not os.path.exists(directoryString):
        print("must be a working directory\n")
        main()
    searchString = input('Search: ')
    search(directoryString, searchString.lower())

def search(directoryString, searchString):
    foundBool = False
    # search and output
    os.chdir(directoryString)
    for file in os.listdir(directoryString):
        if os.path.isfile(file):
            try:
                with open(file, 'r') as fileinput:
                    count = 1
                    for count, line in enumerate(fileinput):
                        lineStr = line.lower()
                        if searchString in lineStr:
                            foundBool = True
                            basename = os.path.basename(file)
                            if len(basename) > 35:
                                basename = basename[0:34] + '...'
                            print('File {}: Line {}: {}'.format(basename, count, line))
            except IOError as e:
                if e.errno == errno.ENOENT:
                    print(os.path.basename(file), ' does not exist')
                if e.errno == errno.EACCES:
                    print(os.path.basename(file), ' cannot be read')
                else:
                    print(os.path.basename(file), e)
    if foundBool is False:
        print('**NO WORDS FOUND**')

main()

