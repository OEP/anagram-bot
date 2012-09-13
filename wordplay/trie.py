

class Trie:

  def __init__(self):
    self._root = Trie.Node(None,None)
  
  def has(self, key):
    """Returns true if 'key' is present in trie."""
    if len(key) == 0 or key == None:
      raise ValueError("Key can't be length 0 or None.")
    node = self._root
    for c in key:
      if node == None:
        return False
      node = node._get(c)
    return node != None and node._isTerminal()
  
  def addWord(self, word):
    """Adds word to the trie."""
    node = self._root
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

    def keys(self):
      return self._nextMap.keys()

    def _flagTerminal(self):
      self._nextMap[None] = None

    def _isTerminal(self):
      return None in self._nextMap

    def _get(self, letter):
      return self._nextMap.get(letter)

    def _setDefault(self, letter):
      return self._nextMap.setdefault(letter, Trie.Node(self, letter))

    def __str__(self):
      return self._letter

    def __repr__(self):
      return self.__str__() + " (terminal)" if self._isTerminal() \
        else " (nonterminal)"
