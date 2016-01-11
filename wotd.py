import random

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

def wotd():
	with open('combinedlist.txt', 'r') as words:
		with open('previouswords.txt', 'r+') as hist:
			wordlist = words.readlines()
			histlist = hist.readlines()
			while len(wordlist) > 0:
				wotd = wordlist.pop(random.randrange(len(wordlist)))
				if wotd not in histlist:
					hist.write(wotd)
					histlist.append(wotd)
					
def main():
	wotd()
	
if __name__ == "__main__":
	main()