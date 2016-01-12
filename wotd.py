import random
import praw
from datetime import date
import login
import re
import urllib.request
import time
import definitionfinder

"""
Basically I need to log onto reddit with a bot and constantly be looking for the
word of the day in all submitted comments (if possible). Once someone uses the word,
reply to them with "blah blah blah" and then basically we can just have it sleep
until the next day.
"""

# This method is only for comparing the reference list with the created list.
# I wanted to make sure that there weren't any words missing/extras added.

def compareLists():
	wotd = open('previouswords.txt', 'r')
	base = open('combinedlist.txt', 'r')
	baselist = base.readlines()
	wotdlist = wotd.readlines()
	wotdlist.sort()
	counter = 0
	wotdcounter = 0
	basecounter = 0
	while wotdcounter != len(wotdlist):
		if wotdlist[wotdcounter] == baselist[basecounter]:
			counter += 1
		else:
			print("Dictionary: %s WOTD: %s" % (wotdlist[wotdcounter].encode("utf-8"), baselist[basecounter].encode("utf-8")))
			break
		wotdcounter += 1
		basecounter += 1
	print(counter)
	
# A method to look through the created list and search for any doubles.
# Outputs to doubleCounter.txt.

def findDoubles():
	with open('previouswords.txt', 'r') as input:
		doubleCounter = {}
		for line in input:
			if line not in doubleCounter:
				doubleCounter[line.strip()] = 1
			else:
				doubleCounter[line.strip()] += 1
		output = open('doubleCounter.txt', 'w')
		for key, value in doubleCounter.items():
				if value > 1:
					output.write("%20s: %d\n" % (key, value))
		output.close()
		
# Using the list of reference words, this picks a random word from the list.
# If the word picked has not been picked before (is not in previouswords.txt),
# It will add the word to previouswords.txt.
# Continues until all words have been used up.

def wotdFinder():
	with open('combinedlist.txt', 'r') as words, open('previouswords.txt', 'r+') as hist:
		wordlist = words.read().splitlines() #List of words to pick a WOTD from.
		datelist = []
		histlistwords = []
		for line in hist:
			splitwords = line.split(': ')
			datelist.append(splitwords[0])
			histlistwords.append(splitwords[1][:-1])
		s = set(histlistwords)
		usewords = [x for x in wordlist if x not in s]
		#If the previously picked WOTD list is empty, or it's last line doesn't contain today's date:
		if date.today().strftime("%b %d %Y") not in datelist and len(usewords) != 0:
			wotd = usewords.pop(random.randrange(len(usewords))) #Pop a random word from wordlist.
			hist.write("%s: %s\n" % (date.today().strftime("%b %d %Y"), wotd))
			print(wotd.encode('utf-8'))
			return wotd
		else:
			return histlistwords.pop()

def getDefinition(word):
	definitionfinder.definition(word)
	definition = ""
	with open('def.txt', 'r') as deffile:
		definition = deffile.read()
	comment.reply(
		"Congratulations! You have used the word of the day: %s.\n\n %s is defined as: %s\n\n I don't actually have a prize for you, so have some internet brownie points!\n\n ------------------------- \n\n This bot is in beta, so if you see any bugs, errors, or have any suggestions, feel free to contact /u/joshjayk or just PM the bot itself. Thanks!" % (word.capitalize(), word.capitalize(), definition))
		
def commentPoster():
	wordbot = login.login()
	wordbot.config.api_request_delay = 1
	currentDay = date.today()
	word = wotdFinder()
	wordfinder = re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search
	comments = praw.helpers.comment_stream(wordbot, 'all')
	commentFound = 0
	for comment in comments:
		word = wotdFinder()
		if wordfinder(comment.body) is not None:
			print("Word found: %s" % comment.body.encode("utf-8"))
			getDefinition(word)
			commentFound = 1
			break
	if commentFound == 1:
		while date.today() == currentDay:
			time.sleep(1)
	
	
def main():
	while True:
		commentPoster()
	
if __name__ == "__main__":
	main()