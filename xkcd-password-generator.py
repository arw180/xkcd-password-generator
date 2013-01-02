#!/usr/bin/env python
# encoding: utf-8

"""
xkcd-password-generator: create simple, secure, dictionary-based passwords that 
are easy to remember and hard for computers to guess. Inspired by the xkcd 
comic: http://xkcd.com/936/

Copyright (c) 2013
Alan Ward <arw180@gmail.com>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""


"""
#TODO:
Use ssl.RAND_bytes(num) to generate random numbers 
 (cryptographically strong pseudo-random generator)

Add an interactive mode
"""

import argparse
import re
import random
import textwrap
import sys
from math import log, floor

# Minimum recommended number of words to choose from for a secure password
MIN_WORD_BANK = 1024   

def main ():
    """ main operation """
    args = parse_args()
    words = read_word_list (args.word_list_file)
    wordListLength = len(words)
    
    if args.verbose:
        verbose_report(wordListLength, args.words)
    
    password = choose_words(words, args.words)
    output_password(password, wordListLength)
    
    
def parse_args ():
    """ Parse input arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('word_list_file', 
    help='filename (with absolute path) to \
    file containing word list (one word per line)')
    parser.add_argument('-w', '--words', default=4,  type=int, help='number of \
    words to use in the password (default is 4)' )
    parser.add_argument('-v', '--verbose', help="verbose output", 
                        action="store_true")
    
    args = parser.parse_args()
    validate_args(args)
    return args

# 
def read_word_list (wordListFile):
    """
    Open the file provided in the command-line options that contains the 
    set of all words to be pulled from for password generation.
    This file need not adhere to any particular format. All special characters 
    (non-letters) will be stripped, and all words converted to lower-case. 
    Duplicate words will be deleted.
    """
    words = []
    
    try:
        with open(wordListFile, 'r') as f: 
            for line in f:
                words_on_line = line.split()
                for w in words_on_line:
                    w = re.sub('[^a-zA-Z]','', w)
                    w = w.lower()
                    if w is not '\n' and w is not ' ' and w is not '':
                        words.append(w)
    except Exception:
        sys.stderr.write('Unable to open wordlist file - exiting.\n')
        sys.exit(1)
    
    # Remove duplicate words
    return set(words)
    

def choose_words (words, numberOfWords):
    """
    Selects the words at random to use for the password. Note that in its 
    current implementation, this is not technically cryptographically secure, 
    but shouldn't be an issue for users using this script on their own 
    computers. 
    """
    return random.sample(words, numberOfWords)

def verbose_report (wordListLength, numWords):
    """
    Reports how many unique words were found in the given input file and 
    provides information on the entropy of the password that is created.
    """
    wordListLengthStr = str(wordListLength)
    entropyPerWord = round(log(wordListLength, 2),1)
    totalEntropy = round(log(wordListLength, 2),1)*numWords
    bruteForceTrials = floor(pow(2,floor(totalEntropy))/2)
    bruteForceTrialsStr = str('%.2e' % bruteForceTrials)
    secondsInAYear = 60*60*24*7*52
    yearsToCrack = bruteForceTrials/(1000*secondsInAYear)
    numWordsStr = str(numWords)
    print('Choosing password from a list of ' + wordListLengthStr + 
          ' unique words')

    msg = 'Using a list of ' + wordListLengthStr + \
    ' words yields an entropy of ' +  \
    str(entropyPerWord) + \
    ' bits per word. Using ' + \
    numWordsStr + \
    ' words from the list yields a password with ' + \
    str(totalEntropy) + \
    ' bits of entropy. A brute force attacker would, on average, need ' + \
    bruteForceTrialsStr + ' attempts to crack your password. ' + \
    'At 1000 guesses per second, that will take approximately ' + \
    str(int(yearsToCrack)) + ' years to crack.' 
    
    print(textwrap.fill(msg))
    
def output_password(password, wordListLength):
    """
    Outputs the password to stdout
    """
    formatted_password = ''
    for word in password:
        word += ' '
        formatted_password += word
        
    if (wordListLength < MIN_WORD_BANK):
        print('WARNING: Word list only contains ' + str(wordListLength) + 
          ' words, which is not long enough to guarantee a secure password')
    print ('************************************************************\n \
    PASSWORD: ' + formatted_password + \
    '\n************************************************************')
    
def validate_args (args):
    """ Validates input arguments """
    if args.words < 1:
        sys.stderr.write('Invalid number of words for password\n')
        sys.exit(1)
    
if __name__ == '__main__':
    main()