"""
Wraps the 'an' executable.
"""

from subprocess import call
import random
import os
import anagram

GOOD_NUMBER = 32000
GOOD_MINIMUM = 3

def pickRandom(cipher):
  tmp = friendly_an(cipher)
  if len(tmp) == 0:
    return None
  return random.choice(tmp)

def friendly_an(cipher,
  dictionary=None,
  words=False,
  contains=None,
  minimum=GOOD_MINIMUM,
  used=None,
  length=None,
  number=GOOD_NUMBER):
  """Wraps 'good' parameters."""

  length = len(cipher.split(" "))

  return an(cipher,
    dictionary,
    words,
    contains,
    minimum,
    used,
    length,
    number)

def an(cipher,
  dictionary=None,
  words=False,
  contains=None,
  minimum=None,
  used=None,
  length=None,
  number=None):

  cipher = anagram.filterCipher(cipher)
  
  tmpFile = "/tmp/an." + str(random.randint(1,3000))
  fp = open(tmpFile, "w+")
  
  if not tmpFile:
    raise IOError("Can't open " + tmpFile)

  command = ["an"]

  if dictionary: command.extend(["-d", str(dictionary)])
  if words: command.extend(["-w"])
  if contains: command.extend(["-c", str(contains)])
  if minimum: command.extend(["-m", str(minimum)])
  if used: command.extend(["-u", str(used)])
  if length: command.extend(["-l", str(length)])
  if number: command.extend(["-n", str(number)])

  command.append(cipher)

  call(command, stdout=fp)

  fp.seek(0)
  anagrams = []
  for line in fp:
    anagrams.append(line.strip())

  fp.close()

  os.remove(tmpFile)
  return anagrams
