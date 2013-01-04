# xkcd-password-generator
=======================

A simple password generator inspired by xkcd - http://xkcd.com/936/

Run the script from the command-line, passing in a file containing the list of all possible words to use for password generation. The file doesn't need to be structured in any particular way - all non-letter characters will be removed (as will duplicate words), and the letters will be set to all lower-case. Two files containing the 'most common' 1,000 and 5,000 english words are included for convenience, but any file can be used.


## Usage 

````
./xkcd-password-generator.py <word_list_file>
````

### Options:

 * `-v, --verbose` - report the number of words found in the word file and the resulting entropy of the password
 * `-n, --numwords` - set the number of words to use for each generated password. The default value is 4
 * `--min` - minimum number of letters in any word used in the password
 * `--max` - maximum number of letters in any word used in the password

Example usage:

````
./xkcd-password-generator.py wordListTop1000.txt
````
output:
````
************************************************************
     PASSWORD: on mouth heard swim 
************************************************************
````

Another example:

````
./xkcd-password-generator.py wordListTop1000.txt -v --min 2 --max 8 -n 5
````
Output:
````
Choosing password from a list of 980 unique words
Using a list of 980 words yields an entropy of 9.9 bits per word.
Using 5 words from the list yields a password with 49.5 bits of
entropy. A brute force attacker would, on average, need 2.81e+14
attempts to crack your password. At 1000 guesses per second, that will
take approximately 8950 years to crack.
************************************************************
     PASSWORD: noise form guide else company 
************************************************************
````

## Requirements
Tested with Python 2.7.2

## License
MIT Licensed
