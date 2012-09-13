"""
Wordplay class.
"""

import string
import random

from trie import Trie

anagram_characters = string.ascii_letters

def _deductKey(someDict, letter, amt=1):
  """Creates a copy of 'someDict', deducts key 'letter' and deletes."""
  tmpDict = dict(someDict)
  tmpDict[letter] -= amt
  if tmpDict[letter] <= 0:
    del tmpDict[letter]
  return tmpDict

def filterCipher(charsequence):
  """Returns allowed set of anagram characters in 'charsequence'."""
  return filter(lambda x: x in anagram_characters, charsequence)

class Wordplay:

  DEFAULT_MAX = 0
  DEFAULT_KEY = lambda x:x

  END_FRONT = 1
  END_REAR = 2
  END_BOTH = 3

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
      self._addWord(word)
    fp.close()

  def has(self, word):
    return self._forwardTrie.has(word) and \
      self._reverseTrie.has(word[::-1])

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

  def solveAnagram(self, cipher, maxSolutions=DEFAULT_MAX, sortKey=DEFAULT_KEY):
    charMap = self._formatCipher(cipher)
    solutions = 0

    for solution in self._solveAnagramEntry(charMap, sortKey):
      solutions += 1
      yield solution
      if solutions >= maxSolutions and maxSolutions > 0:
        break

  def solvePalindrome(self, cipher, maxSolutions=DEFAULT_MAX,
    sortKey=DEFAULT_KEY):
    charMap = self._formatCipher(cipher)
    solutions = 0
    for solution in self._solvePalindromeEntry(charMap,sortKey):
      solutions += 1
      yield solution
      if solutions >= maxSolutions and maxSolutions > 0:
        break

  def _solvePalindromeEntry(self, charMap, sortKey, froot=None, rroot=None):
    if froot == None: froot = self._forwardTrie._root
    if rroot == None: rroot = self._reverseTrie._root
    #print "entry", froot, rroot
    keys = set(charMap.keys()) & \
      set(froot.keys()) & \
      set(rroot.keys())

    for key in sorted(keys, key=sortKey):
      fnode = froot._get(key)
      rnode = rroot._get(key)
      for solution in self._solvePalindromeRecursive(charMap, sortKey, fnode,
        rnode):
        yield solution

  def _solvePalindromeRecursive(self, charMap, sortKey, fnode, rnode):
    #print "recur", fnode, rnode
    count = min(charMap[fnode._letter], 2)
    tmpMap = _deductKey(charMap, fnode._letter, count)
    keys = set(tmpMap.keys()) & \
      set(rnode.keys()) & \
      set(fnode.keys())

    if fnode._isTerminal() and self.canRecur():
      keys.add(Wordplay.END_FRONT)

    if rnode._isTerminal() and self.canRecur():
      keys.add(Wordplay.END_REAR)

    if rnode._isTerminal() and fnode._isTerminal() and self.canRecur():
      keys.add(Wordplay.END_BOTH)
    
    if len(tmpMap) == 0 and self._validWord(fnode, rnode, count*fnode._letter):
      yield count*fnode._letter
    elif len(tmpMap) == 0:
      pass
    elif len(keys) == 0:
      pass
    else:
      for key in sorted(keys, key=sortKey):
        solutionGen = None
        prefix = fnode._letter
        suffix = rnode._letter

        if key == Wordplay.END_FRONT:
          solutionGen = self._solvePalindromeEntry(tmpMap, sortKey, None,
            rnode)
          prefix += " "
        elif key == Wordplay.END_REAR:
          solutionGen = self._solvePalindromeEntry(tmpMap, sortKey, fnode,
            None)
          suffix = " " + suffix
        elif key == Wordplay.END_BOTH:
          solutionGen = self._solvePalindromeEntry(tmpMap, sortKey)
          suffix = " " + suffix
          prefix += " "
        else:
          recurFNode = fnode._get(key)
          recurRNode = rnode._get(key)
          solutionGen = self._solvePalindromeRecursive(tmpMap, sortKey,
            recurFNode, recurRNode)

        for subSolution in solutionGen:
          if subSolution != None:
            yield prefix + subSolution + suffix

  def _validWord(self, fnode, rnode, middle):
    while fnode._parent and fnode._parent._letter != None:
      fnode = fnode._parent
      middle = fnode._letter + middle

    while rnode._parent and rnode._parent._letter != None:
      rnode = rnode._parent
      middle = middle + rnode._letter

    return self.has(middle)

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
    for c in filterCipher(cipher).upper():
      charmap[c] = 1 + charmap.get(c, 0)
    return charmap


  def _addWord(self, word):
    word = word.strip().upper()
    if len(word) < self._minWordSize:
      return
    self._forwardTrie.addWord(word)
    self._reverseTrie.addWord(word[::-1])



