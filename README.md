# WOTDBot
A reddit bot for words of the day.
Files:

wotd.py - The main program. Runs the bot and looks for the WOTD in the reddit comment stream. Once found, it comments and then goes to sleep until the next day, where it chooses a new word.

definitionfinder.py - The program that scrapes www.dictionary.com for the definition of any word. Removes any HTML jargon and returns all definitions with examples.