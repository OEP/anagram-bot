"""
Wordplay class.
"""

import string
import random

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

    self._minWordSize = minWordSize
    self._multipleWords = multipleWords
    self._roots = dict()

    fp = open(wordlist)

    for word in fp:
      self._addWord(word.upper().strip())

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

  def has(self, key):
    """Returns true if 'key' is present in trie."""
    if len(key) == 0 or key == None:
      raise ValueError("Key can't be length 0 or None.")
    node = self._getRoot(key[0])
    for c in key[1:]:
      if node == None:
        return False
      node = node._get(c)
    return node != None and node._isTerminal()
    


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

  def _getRoot(self, char):
    """Returns a root node representing 'char'."""
    return self._roots.get(char, None)

  def _setDefault(self, char):
    """Returns root node for 'char' or create if it does not exist."""
    return self._roots.setdefault(char, Wordplay.Node(self, char))

  def _addWord(self, word):
    """Adds word to the trie."""
    if len(word) < self._minWordSize:
      return

    node = None
    for c in word:
      if node == None:
        node = self._setDefault(c)
      else:
        node = node._setDefault(c)

    node._flagTerminal()
      


  class Node:
    
    def __init__(self, parent, letter):
      self._letter = letter
      self._nextMap = dict()
      self._parent = parent

    def solve(self, charMap, sortKey):
      tmpMap = _deductKey(charMap, self._letter)
      keys = set(tmpMap.keys()) & set(self._nextMap.keys())

      if self._isTerminal() and self._parent.canRecur():
        keys.add(None)

      if len(tmpMap) == 0 and self._isTerminal():
        yield self._letter
      elif len(tmpMap) == 0:
        pass
      else:
        for key in sorted(keys, key=sortKey):
          solutionGen = None
          prefix = self._letter

          if key == None:
            solutionGen = self._parent._solveRecursive(tmpMap, sortKey)
            prefix += " "
          else:
            node = self._get(key)
            solutionGen = node.solve(tmpMap, sortKey)

          for subSolution in solutionGen:
            if subSolution != None:
              yield prefix + subSolution

    def _flagTerminal(self):
      self._nextMap[None] = None

    def _isTerminal(self):
      return None in self._nextMap

    def _get(self, letter):
      return self._nextMap.get(letter)

    def _setDefault(self, letter):
      return self._nextMap.setdefault(letter, Wordplay.Node(self._parent, letter))

    def __str__(self):
      return self._letter

    def __repr__(self):
      return self.__str__() + " (terminal)" if self._isTerminal() \
        else " (nonterminal)"
