"""
Wordplay class.
"""

import string
import random

from trie import Trie

anagram_characters = string.ascii_letters

def _deductKey(someDict, letter):
  """Creates a copy of 'someDict', deducts key 'letter' and deletes."""
  tmpDict = dict(someDict)
  tmpDict[letter] -= 1
  if tmpDict[letter] <= 0:
    del tmpDict[letter]
  return tmpDict

def filterCipher(charsequence):
  """Returns allowed set of anagram characters in 'charsequence'."""
  return filter(lambda x: x in anagram_characters, charsequence)

class Wordplay:

  DEFAULT_MAX = 1
  DEFAULT_KEY = lambda x:x

  def __init__(self,
    wordlist='/usr/share/dict/words',
    multipleWords=False,
    minWordSize=1):

    self._reverseTrie = Trie()
    self._forwardTrie = Trie()

    self._minWordSize = minWordSize
    self._multipleWords = multipleWords

    fp = open(wordlist)
    for word in fp:
      self._addWord(word.upper().strip())
      ## TODO: Reverse trie
    fp.close()

  def pickRandom(self, cipher):
    """Picks a random anagram of cipher and returns it or None."""
    result = list(self.solveRandom(cipher,1))
    if len(result) == 0: return None
    return result[0]

  def pickFirst(self, cipher):
    """Picks the first anagram it can find."""
    result = list(self.solve(cipher,1))
    if len(result) == 0: return None
    return result[0]
  
  def solveRandom(self, cipher, maxSolutions=DEFAULT_MAX):
    return self.solve(cipher, maxSolutions, lambda x: random.random())

  def canRecur(self):
    return self._multipleWords

  def solve(self, cipher, maxSolutions=DEFAULT_MAX, key=DEFAULT_KEY):
    charmap = self._formatCipher(filterCipher(cipher))
    solutions = 0

    for solution in self._solveRecursive(charmap, key):
      if solutions >= maxSolutions:
        break
      yield solution

  def _solveRecursive(self, charmap, key):
    keys = set(charmap.keys()) & set(self._roots.keys())
    for char in sorted(keys, key=key):
      for solution in self._roots[char].solve(charmap, key):
        if solution != None:
          yield solution
  
  def _formatCipher(self, cipher):
    charmap = dict()
    for c in cipher.upper():
      charmap[c] = 1 + charmap.get(c, 0)
    return charmap


  def _addWord(self, word):
    word = word.strip().upper()
    if len(word) < self._minWordSize:
      return
    self._forwardTrie.add(word)
    ## TODO: Add reverse trie



