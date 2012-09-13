#!/usr/bin/env python

import sys

from wordplay.wordplay import Wordplay

def printUsage(progName):
  print "Usage: %s [cipher1] [cipher2] ..." % progName

def main():
  if len(sys.argv) < 2:
    printUsage(sys.argv[0])
    sys.exit(1)

  wp = Wordplay('wordlists/simple.txt', multipleWords=True)

  for cipher in sys.argv[1:]:
    count = 0
    for palindrome in wp.solvePalindrome(cipher):
      if len(sys.argv) > 2 and count == 0:
        print "Palindromes of: %s" % cipher
      count += 1
      print palindrome
    if count == 0:
      print "No palindromes found for %s" % cipher

if __name__ == "__main__":
  main()
