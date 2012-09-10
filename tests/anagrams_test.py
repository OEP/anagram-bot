import unittest

from anagram_bot import anagram

class AnagramTests(unittest.TestCase):

  WORDLIST1 = 'wordlists/test1.txt'
  WORDLIST2 = 'wordlists/test2.txt'
  SOLUTION2 = 'wordlists/result2.txt'

  def setUp(self):
    self._anagram1 = anagram.Anagram(AnagramTests.WORDLIST1)
    self._anagram2 = anagram.Anagram(AnagramTests.WORDLIST2)

  def test_oneWord(self):
    solution = self._getSolution(AnagramTests.WORDLIST1)
    start = solution[0]
    out = list(self._anagram1.solve(start, len(solution) + 1))
    self.assertEqual(sorted(solution),sorted(out))

  def test_twoWords(self):
    solution = self._getSolution(AnagramTests.SOLUTION2)
    start = solution[0]
    out = list(self._anagram2.solve(start, len(solution) + 1))
    self.assertEqual(sorted(solution), sorted(out))

  def _getSolution(self, filename):
    solution = []
    with open(filename) as fp:
      for line in fp:
        line = line.upper()
        line = line.strip()
        solution.append(line)
    return solution
