import sre, os, getopt, sys

emph = sre.compile("\*(.*?)\*")
regie = sre.compile("\((.*?)\)")
q = sre.compile("\"(.*?)\"")

FILE = "heavenly_credits.txt"

def tex_filtr(line):
	line = emph.sub("\\\\emph{\\1}", line)
	line = regie.sub("(\\\\regie{\\1})", line)
	line = q.sub("\\\\q{\\1}", line)
	return line

def filter_tex(line):
	content = ""
	line = tex_filtr(line[:-1])
	if line.find(": ") >0:
		speaker, text = line.split(": ")
		content += "\speak{%s}{%s}\n" % (speaker, text)
	else:
		if line:
			content += "\\par\\vspace{8pt}\\par\\noindent\\regie{%s}\n" % line
		else:
			content += "\n"
	return content
	
def html_filtr(line):
	line = emph.sub("<em>\\1</em>", line)
	line = regie.sub("(<i>\\1</i>)", line)
	line = q.sub("<q>\\1</q>", line)
	return line
	
def filter_html(line):
	content = ""
	line = html_filtr(line[:-1])
	if line.find(": ") >0:
		speaker, text = line.split(": ")
		content += '<p><b class="speaker">%s:</b> %s</p>\n' % (speaker, text)
	else:
		if line:
			content += '<p class="regie" >%s</p>\n' % line
		else:
			content += "\n"
	return content

def wrap(content, typ):
	template = file("%s.template" % typ).read()
	return template.replace("%%content%%", content)
	
#content = template.replace("%%content%%", content)

#outfh = open("heavenly_credits.tex", 'w')
#outfh.write(content)
#outfh.close()

#os.system("pdflatex heavenly_credits.tex")

def convert(file, typ):
	content = ""
	if typ in ("tex", "html"):
		f = globals()["filter_" + typ]
		content = ''.join(map(f, file))
	return content

def choose_filter(args):
	args, opts = getopt.gnu_getopt(args, "t:h")
	for arg in args:
		if arg[0] == '-t':
			return arg[1]

def get_filter(typ):
	funcname = "filter_" + typ
	if funcname in  globals().keys():
		return globals()[funcname]
	else:
		return lambda x: x

def main():
	typ = choose_filter(sys.argv)
	F = file(FILE)
	content = wrap(convert(F, typ), typ)
	print content
	
if __name__ == "__main__":
	main()
	
