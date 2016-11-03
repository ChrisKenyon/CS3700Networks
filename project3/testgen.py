import argparse
import random

def gen_random_charstring():
    charstring = ""
    length = random.randrange(64)
    for i in range(length):
        char = random.randrange(48, 122)
        charstring += chr(char)
    return charstring

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a txt file of randomly generated text')
    parser.add_argument('-l', '--length', default=10000, help='file length in bytes')
    parser.add_argument('-f', '--filename', default='autotest.txt', help='the filename')
    args = parser.parse_args()

    testfile = open(args.filename, "w")
    charcount = 0
    linecount = 0
    while charcount <= int(args.length):
        writestring = "{} - {}\n".format(linecount, gen_random_charstring())
        charcount += len(writestring)
        if charcount > int(args.length):
            if int(args.length) - charcount > 5:
                break
            else:
                testfile.write(writestring[:int(args.length) - charcount])
        else:
            testfile.write(writestring)
        linecount += 1
    testfile.close()