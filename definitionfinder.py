import urllib.request
import re


def definition(x):
	output = open('def.txt', 'w')
	definition = urllib.request.urlopen("http://dictionary.reference.com/browse/"+x+"?s=t").read().decode("utf-8")
	nohead = definition.split('<div class="def-list">\n')[1]
	notail = nohead.split('tail-wrapper')[0]
	weblist = notail.split('\n')
	header = ''
	deflistcounter = 1
	remove = ['</div>\n', '<li>\n', '</li>\n', '<ol>\n', '</ol>\n', '<div>\n']
	for line in weblist:
		nextline = line
		try:
			nextline = weblist[weblist.index(line) + 1]
		except IndexError:
			nextline = line
		if '<span class="dbox-pg">' in line:	
			header = line.split('<span class="dbox-pg">')[1].split('</span>')[0].lower()
			output.write('\n\n\n\n%s\n\n' % header.title())
		if '<span class="dbox-italic">' in nextline:
			nextline.replace('<span class="dbox-italic">', '*')
			nextline.replace('</span>', '*')
		if '<div class="def-content">' in line and header != 'idioms':
			if 'dbox-example' in nextline:
				defex = nextline.split(': <div class="def-block def-inline-example"><span class="dbox-example">')
				if '<span class="dbox-italic">' in defex[0]:
					defex[0] = defex[0].replace('<span class="dbox-italic">', '')
					defex[0] = defex[0].replace('. </span>', ': ')
				if '<a class="dbox-xref dbox-roman" href=' in defex[0]:
					defex[0] = defex[0].split('>', 1)[1]
					defex[0] = defex[0].split('<')[0]
				if '</span>' in defex[0]:
					defex[0] = ''.join(defex[0].split('</span>'))
				output.write('%d: %s.\n\n' % (deflistcounter, defex[0].capitalize()))
				output.write('\t%s\n\n' % defex[1].split('<')[0].capitalize())
			else:
				defonly = nextline.split(' </div>')[0]
				if '<span class="dbox-italic">' in defonly:
					defonly = defonly.replace('<span class="dbox-italic">', '')
					defonly = defonly.replace('. </span>', ': ')
				if '<a class="dbox-xref dbox-roman" href=' in defonly:
					defonly = re.sub('<a class="dbox-xref dbox-roman" href="(.*?)">', '', defonly)
					defonly = re.sub('</a>', '', defonly)
				output.write('%d: %s\n\n' % (deflistcounter, defonly.capitalize()))
			weblist.remove(line)
			deflistcounter += 1
		if header == 'idioms':
			if '<span class="dbox-bold">' in line:
				idiom = line.split('<span class="dbox-bold">')[1].split(', </span>')[0]
				output.write('%d: %s\n\n' % (deflistcounter, idiom.capitalize()))
				deflistcounter += 1
			elif '<li>' == line:
				idiomdefex = nextline.split(' <div class="def-block def-inline-example"><span class="dbox-example">')
				output.write('\t%s\n\n' % idiomdefex[0].capitalize())
				if len(idiomdefex) == 2:
					output.write('\t\t%s\n\n' % idiomdefex[1].split('</span>')[0].capitalize())
				weblist.remove(line)
	output.close()

def main():
	definition('accredit')
	
if __name__ == "__main__":
	main()