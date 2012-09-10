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
      self._addWord(word)

  def _addWord(self, word):
    if len(word) < self._minWordSize:
      return

    node = None
    for c in word:
      if node == None:
      


  class Node:
    
    def __init__(self, letter):
      self._letter = letter
      self._nextMap = dict()
