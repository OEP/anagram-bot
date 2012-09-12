#!/usr/bin/env python

from bots.base_bot import AnagramBot
from config import USERNAME, PASSWORD, MAINTAINER

def main():
  bot = AnagramBot()
  bot.setMaintainer(MAINTAINER)
  bot.setOutput(AnagramBot.OUT_STDOUT)
  bot.login(USERNAME, PASSWORD)
  bot.makeFunny()

if __name__ == "__main__":
  main()
