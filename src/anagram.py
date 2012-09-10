"""
Anagram class.
"""

class Anagram:
  
  def __init__(self,
    wordlist='/usr/share/dict/words',
    minWordSize=4):

    self._minWordSize = minWordSize
    self._roots = dict()

    fp = open(wordlist)

    for word in fp:
      self._addWord(word.upper().strip())

  def solve(self, cipher, maxSolutions=1, key=lambda x:x):
    charmap = self._formatCipher(cipher)
    keys = set(charmap.keys()) & set(self._roots.keys())
    solutions = 0

    for char in sorted(keys, key=key):
      tmpMap = dict(charmap)
      tmpMap[char] -= 1
      for solution in self._roots[char].solve(tmpMap, key):
        solutions += 1
        yield solution

        if solutions >= maxSolutions:
          break

  
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
    return self._roots.setdefault(char, Anagram.Node(char))

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
    
    def __init__(self, letter):
      self._letter = letter
      self._nextMap = dict()

    def _flagTerminal(self):
      self._nextMap[None] = None

    def _isTerminal(self):
      return None in self._nextMap

    def _get(self, letter):
      return self._nextMap.get(letter)

    def _setDefault(self, letter):
      return self._nextMap.setdefault(letter, Anagram.Node(letter))

    def __str__(self):
      return self._letter

    def __repr__(self):
      return self.__str__()
