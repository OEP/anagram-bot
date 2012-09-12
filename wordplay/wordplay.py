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

  def has(self, word):
    return self._forwardTrie.has(word) ## and TODO: reverseTrie

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

  def solve(self, cipher, maxSolutions=DEFAULT_MAX, sortKey=DEFAULT_KEY):
    charMap = self._formatCipher(filterCipher(cipher))
    solutions = 0

    for solution in self._solveAnagramEntry(charMap, sortKey):
      solutions += 1
      yield solution
      if solutions >= maxSolutions:
        break
  
  def _solveAnagramEntry(self, charMap, sortKey):
    root = self._forwardTrie._root
    keys = set(charMap.keys()) & set(root.keys())

    for key in sorted(keys, key=sortKey):
      node = root._get(key)
      for solution in self._solveAnagramRecursive(charMap, sortKey, node):
        yield solution

  def _solveAnagramRecursive(self, charmap, sortKey, node):
    tmpMap = _deductKey(charmap, node._letter)
    keys = set(tmpMap.keys()) & set(node._nextMap.keys())

    if node._isTerminal() and self.canRecur():
      keys.add(None)

    if len(tmpMap) == 0 and node._isTerminal():
      yield node._letter
    elif len(tmpMap) == 0:
      pass
    elif len(keys) == 0:
      pass
    else:
      for key in sorted(keys, key=sortKey):
        solutionGen = None
        prefix = node._letter

        if key == None:
          solutionGen = self._solveAnagramEntry(tmpMap, sortKey)
          prefix += " "
        else:
          recurNode = node._get(key)
          solutionGen = self._solveAnagramRecursive(tmpMap, sortKey, recurNode)

        for subSolution in solutionGen:
          if subSolution != None:
            yield prefix + subSolution
  
  def _formatCipher(self, cipher):
    charmap = dict()
    for c in cipher.upper():
      charmap[c] = 1 + charmap.get(c, 0)
    return charmap


  def _addWord(self, word):
    word = word.strip().upper()
    if len(word) < self._minWordSize:
      return
    self._forwardTrie.addWord(word)
    ## TODO: Add reverse trie



