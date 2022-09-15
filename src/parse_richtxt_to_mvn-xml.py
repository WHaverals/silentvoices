#!usr/bin/env python
import string, re

rubric = re.compile(r"(\<)([a-zA-Z]+)(\>)")
boundaries = re.compile(r"(\[|\]|\(|\)|\%|\$|\=|\{|\}|\*|\£)")
endings = re.compile(r"(\)|\]|\%|\$|\=|\}|\*|\£)$")
beginnings = re.compile(r"$\(|\[|\{")

name = "Brussels_KBR_3093-3095"

def abbr_to_xml(kind, solution):
	abbr, expan = "", ""
	if kind == "$":
		if "_" in solution:
			val, nr = solution.split("_")
			abbr = '<hi rend="capitalsize'+nr+'">'+val+'</hi>'
		else:
			abbr = '<hi rend="capitalsize1">'+solution+'</hi>'
		expan = abbr
	elif kind == "=":
		abbr = '<num type="roman">'+solution+'</num>'
		expan = abbr
	elif kind == "£":
		abbr = '<g ref="#slongbar"/>'
		expan = "<ex>"+solution+"</ex>"
	elif kind == "*":
		abbr = '<unclear>'+solution+'</unclear>'
		expan = abbr
	elif kind == "(":
		abbr = '<g ref="#bar"/>'
		expan = "<ex>"+solution+"</ex>"
	elif kind == "[":
		if solution == "ist":
			abbr = 'p<g ref="#bar"/>'
			expan = "<ex>"+solution+"</ex>"
		else:
			abbr = '<g ref="#apomod"/>'
			expan = "<ex>"+solution+"</ex>"
	elif kind == "{":
		if solution == "et" or solution == "at":
			abbr = '<g ref="#etfin"/>'
		elif solution == "pro":
			abbr = '<g ref="#pflour"/>'
		elif solution == "par":
			abbr = '<g ref="#pbardes"/>'
		elif solution == "per":
			abbr = '<g ref="#pbardes"/>'
		elif solution == "con" or solution == "us" or solution == "com":
			abbr = '<g ref="#usmod"/>'
		expan = "<ex>"+solution+"</ex>"
	elif kind == "%":
		if solution == "rv":
			abbr = '<hi rend="superscript">v</hi>'
			expan = "<ex>"+solution+"</ex>"
		elif solution == "ri":
			abbr = '<hi rend="superscript">i</hi>'
		elif solution == "ur":
			abbr = '<hi rend="superscript">z</hi>'
		elif solution == "ue":
			abbr = '<hi rend="superscript">e</hi>'
			expan = "<ex>"+solution+"</ex>"
		elif solution == "ro":
			abbr = '<hi rend="superscript">o</hi>'
			expan = "<ex>"+solution+"</ex>"
		elif solution == "ua":
			abbr = '<hi rend="superscript">u</hi>'
			expan = "<ex>"+solution+"</ex>"
		elif solution == "ra":
			abbr = '<hi rend="superscript">u</hi>'
			expan = "<ex>"+solution+"</ex>"
		elif solution == "re":
			abbr = '<hi rend="superscript">e</hi>'
			expan = "<ex>"+solution+"</ex>"
		elif solution == "eit" or solution == "iet":
			abbr = '<hi rend="superscript">t</hi>'
			expan = "<ex>"+solution+"</ex>"
		else:
			abbr = '<hi rend="superscript">'+solution+'</hi>'
			expan = "<ex>"+solution+"</ex>"
	return abbr, expan

def parse_abbrevs(word):
	# insert dummy boundary marker:
	w = boundaries.sub(r"|\1", word)
	if not "|" in w:
		return word
	abbr = ""
	expan = ""
	prev_kind = ""
	for part in w.split("|"):
		part = endings.sub("", part).strip()
		if not part:
			continue
		if (part[0] == "%" and prev_kind == "%") or \
			(part[0] == "$" and prev_kind == "$") or \
			(part[0] == "=" and prev_kind == "=") or \
			(part[0] == "*" and prev_kind == "*") or \
			(part[0] == "£" and prev_kind == "£") or \
			(part[0] in ")]}"):
			part = part[1:]		
		if part:
			if part[0] in "({[%$=*£":
				kind = part[0]
				prev_kind = kind
				solution = part[1:]
				a, e = abbr_to_xml(kind, solution)
				abbr += a
				expan += e
			else:
				abbr += part
				expan += part
	if abbr != expan:
		abbr = "<abbr>"+abbr+"</abbr>"
		expan = "<expan>"+expan+"</expan>"
		return '<choice>'+abbr+expan+'</choice>'
	else:
		return abbr

def main():
	lines = [line.strip() for line in open("ms_orig.txt", 'r').readlines() if line.strip()]
	xml = ""
	for line in lines:
		line = line.replace(">", "$").replace("<", "$")
		if line.startswith("&"):
			curr_page_nr = line.replace("&", "")
			xml+='\n\n<pb xml:id="'+name+'.f'+curr_page_nr+'" n="'+curr_page_nr+'"/>\n'
			line_counter = 0
		else:
			line_counter+=1
			trailer = ""
			if line.endswith("#"):
				trailer += '<choice><sic></sic><corr><c type="shy">-</c></corr></choice>'
				line = line[:-1]
			words = line.split()
			xml += '<lb n="'+str(line_counter)+'" xml:id="'+name+'f'+str(curr_page_nr)+'.'+str(line_counter)+'"/>'
			for i, word in enumerate(words):
				if word in string.punctuation:
					xml += '<pc>'+word+'</pc> '
				else:
					xml += parse_abbrevs(word)+" "
			xml = xml.strip()
			xml = xml.replace("C|", '<g ref="#para"/>')
			xml+=trailer
			xml+="\n"
	
	header = open("header.txt", 'r').read()
	footer = open("footer.txt", 'r').read()
	with open("ms.xml", "w+") as F:
		F.write(header+xml+footer)

#print(parse_abbrevs("=xl="))
#print(parse_abbrevs("mi(n)ne(n)"))
#print(parse_abbrevs("c%rv%ce"))
main()