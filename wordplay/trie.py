

class Trie:

  def __init__(self):
    self._roots = dict()
  
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
  
  def addWord(self, word):
    """Adds word to the trie."""
    node = None
    for c in word:
      if node == None:
        node = self._setDefault(c)
      else:
        node = node._setDefault(c)
    node._flagTerminal()

  def _getRoot(self, char):
    """Returns a root node representing 'char'."""
    return self._roots.get(char, None)

  def _setDefault(self, char):
    """Returns root node for 'char' or create if it does not exist."""
    return self._roots.setdefault(char, Trie.Node(self, char))
  
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
