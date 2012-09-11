import reddit
import random
import anagram
import re
import string

def _matchCase(model, text):
  i = 0
  j = 0
  out = ""
  while i < len(model) and j < len(text):
    if model[i] in string.ascii_uppercase:
      out += text[j].upper()
      j += 1
    elif model[i] in string.ascii_lowercase:
      out += text[j].lower()
      j += 1
    i += 1
  if j < len(text):
    out += text[j:].lower()
  return out

class AnagramBot:

  def __init__(self):
    self._reddit = reddit.Reddit(user_agent='anagram_bot')
    self._anagram = anagram.Anagram()

  def makeFunny(self):
    comments = list(self._fetchComments())
    attempts = 0
    anagrams = []

    while len(anagrams) == 0 and attempts < 10:
      attempts += 1
      comment = random.choice(comments)
      anagrams = self._attempt(comment.body)

    if len(anagrams) == 0:
      return None

    reply = self._replace(comment.body, anagrams)

    print comment.body
    print "=================================="
    print reply

  def _replace(self, text, anagrams):
    for anagram in anagrams:
      pattern = "([^A-Za-z'0-9])" + anagram[0] + "([^A-Za-z'0-9])"
      replace = "\\1" + anagram[1] + "\\2"
      text = re.sub(pattern, replace, text)
    return text

    
  def _attempt(self, text):
    result = []
    noMatches = True
    for match in re.findall("[A-Za-z'0-9]+", text):
      for anagram in self._anagram.solveRandom(match, 5):
        if anagram != None and anagram != match.upper():
          anagram = _matchCase(match, anagram)
          result.append( (match, anagram) )
    return result
  
  def _fetchComments(self):
    return self._reddit.get_all_comments()


    

