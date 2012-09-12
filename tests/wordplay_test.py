import unittest

from wordplay.wordplay import Wordplay

class WordplayTest(unittest.TestCase):

  WORDLIST1 = 'wordlists/test1.txt'
  WORDLIST2 = 'wordlists/test2.txt'
  SOLUTION2 = 'wordlists/result2.txt'

  def setUp(self):
    self._anagrams = dict()
    self.get(WordplayTest.WORDLIST1)
    self.get(WordplayTest.WORDLIST2)


  def get(self, path):
    return self._anagrams.setdefault(path, Wordplay(path,
      multipleWords=True))

  def test_aaBuiltCorrectly(self):
    for pair in self._anagrams.items():
      path = pair[0]
      anagram = pair[1]

      words = self._getLines(path)
      for word in words:
        self.assertTrue( anagram.has(word) )
    

  def test_oneWord(self):
    anagram = self.get(WordplayTest.WORDLIST1)
    solution = self._getLines(WordplayTest.WORDLIST1)
    start = solution[0]
    out = list(anagram.solve(start, len(solution) + 1))
    self.assertEqual(sorted(solution),sorted(out))

  def test_twoWords(self):
    anagram = self.get(WordplayTest.WORDLIST2)
    solution = self._getLines(WordplayTest.SOLUTION2)
    start = solution[0]
    solution = set(solution)
    out = set(anagram.solve(start, len(solution) + 30))
    self.assertEqual(solution, out)

  def _getLines(self, filename):
    solution = []
    with open(filename) as fp:
      for line in fp:
        line = line.upper()
        line = line.strip()
        solution.append(line)
    return solution
