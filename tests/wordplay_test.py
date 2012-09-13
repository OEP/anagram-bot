import unittest
import random

from wordplay.wordplay import Wordplay

class WordplayTest(unittest.TestCase):

  WORDLIST1 = 'wordlists/test1.txt'
  WORDLIST2 = 'wordlists/test2.txt'
  SOLUTION2 = 'wordlists/result2.txt'
  PALINDROMES = 'wordlists/one-word-palindromes.txt'
  BIGPALINDROME = 'wordlists/big-palindrome.txt'
  SOLUTION_BIGPALINDROME = 'wordlists/result-big-palindrome.txt'
  SIMPLE = 'wordlists/simple.txt'

  def setUp(self):
    self._anagrams = dict()
    self.get(WordplayTest.WORDLIST1)
    self.get(WordplayTest.WORDLIST2)
    self.get(WordplayTest.PALINDROMES)
    self.get(WordplayTest.BIGPALINDROME)

  def _simplePalindrome(self, wp):
    charList = list("WASITABARORABATISAW")
    random.shuffle(charList)

    solution = set(self._getLines(WordplayTest.SOLUTION_BIGPALINDROME))
    for out in wp.solvePalindrome("".join(charList),200):
      self.assertTrue(out in solution)

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

  def test_simplePalindrome(self):
    wp = self.get(WordplayTest.PALINDROMES)
    for palindrome in self._getLines(WordplayTest.PALINDROMES):
      out = list( wp.solvePalindrome(palindrome) )
      self.assertTrue( palindrome in out )

  def test_bigPalindrome(self):
    wp = self.get(WordplayTest.BIGPALINDROME)
    self._simplePalindrome(wp)

  def test_realWorld(self):
    wp = self.get(WordplayTest.SIMPLE)
    self._simplePalindrome(wp)

  def test_oneWord(self):
    anagram = self.get(WordplayTest.WORDLIST1)
    solution = self._getLines(WordplayTest.WORDLIST1)
    start = solution[0]
    out = list(anagram.solveAnagram(start, len(solution) + 1))
    self.assertEqual(sorted(solution),sorted(out))

  def test_twoWords(self):
    anagram = self.get(WordplayTest.WORDLIST2)
    solution = self._getLines(WordplayTest.SOLUTION2)
    start = solution[0]
    solution = set(solution)
    out = set(anagram.solveAnagram(start, len(solution) + 30))
    self.assertEqual(solution, out)

  def _getLines(self, filename):
    solution = []
    with open(filename) as fp:
      for line in fp:
        line = line.upper()
        line = line.strip()
        solution.append(line)
    return solution
