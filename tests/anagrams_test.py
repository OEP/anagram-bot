import unittest

from anagram_bot import anagram

class AnagramTests(unittest.TestCase):

  WORDLIST1 = 'wordlists/test1.txt'

  def setUp(self):
    self._anagram1 = anagram.Anagram(AnagramTests.WORDLIST1)

  def test_oneWord(self):
    words = []
    with open(AnagramTests.WORDLIST1) as fp:
      for word in fp:
        words.append(word)

    start = words[0]

    for i in self._anagram1.solve(start, len(words)):
      print i
