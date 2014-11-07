#!/usr/bin/env python

# collate all reviews for a team into one latex document, then make a PDF

import os,sys

pres_folder = "../presentations/"

def readTex(texInput,region):
	# parse texInput for beginning, middle, or end
	# if region=="begin" use all data up to but not including "\end{document}"
	# if region=="middle" use all data between but not including
	#      "\begin{document}" and "\end{document}"
	# if region=="end" use all data between "\begin{document}" 
	#      and the end of the file
	
	# texInput has all the lines at the moment
	foundBeginDoc = False
	foundEndDoc = False
	
	parsedText = ""
	for line in texInput:
		if "begin{document}" in line:
			foundBeginDoc = True
		if "end{document}" in line:
			foundEndDoc = True
		if region!="end" and foundEndDoc:
			break
		if region != "begin" and not foundBeginDoc:
			continue
		if region != "begin" and "begin{document}" in line:
			continue
		parsedText+=line
	return parsedText

if (len(sys.argv) != 3):
	print "usage: collateScores date teamName"
	print "  where 'date' is in the form yyyy-m-d"
	sys.exit(1)

date = sys.argv[1]
teamName = sys.argv[2]

print "Collating scores for %s on %s" % (teamName, date)
date_folder = pres_folder+date+"/"
if not os.path.exists(date_folder):
	print "That date doesn't seem to have any entries"
	sys.exit(1)

# folder exists, get directory listing
files = os.listdir(date_folder)

# just include files for this team
files = [x for x in files if teamName in x and "Full_" not in x]

fullLatex = ""
for idx, f in enumerate(files):
	print "Adding %s" % f
	with open(pres_folder+date+"/"+f,"r") as texInputFile:
		texInput = texInputFile.readlines()
		if idx == 0:
			print "begin..."
			fullLatex += readTex(texInput,"begin")
			fullLatex += "\\pagebreak{}\n\n"
		elif idx == len(files)-1:
			print "end..."
			fullLatex += readTex(texInput,"end")
		else:
			print "middle..."
			fullLatex += readTex(texInput,"middle")
			fullLatex += "\\pagebreak{}\n\n"
outputFilename = pres_folder+date+"/Full_"+teamName+"_"+date+".tex"
with open(outputFilename,"w") as f:
	f.write(fullLatex)

# run pdfLatex on the output file to create PDF

outputFolder = pres_folder+date

os.popen('pdflatex -output-directory '+outputFolder+" "+outputFilename).read()
os.popen('cd '+outputFolder+'; rm *.aux *.log')



