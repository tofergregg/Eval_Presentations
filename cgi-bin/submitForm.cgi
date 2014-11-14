#!/usr/bin/env python

import cgi,sys,os
import cgitb
import uuid
import time,datetime
import json
import string

pres_folder = "../presentations/"
latexTemplate="../PresentationTemplate.tex"

cgitb.enable()
	
def collateScores(outputText,form):	
	scoreTypes = [["content","Content"],
			["preparedness","Preparedness"],
			["enthusiasm","Enthusiasm"],
			["vocabulary","Vocabulary"],
			["speaking","Speaking"],
			["organization","Organization"],
			["time","Time\t"],
			["realism","Realistic /"],
			["detail","Detail"],
			["audience","Audience"],
			["overall","Overall"]]
	for scoreType in scoreTypes:
		t,desc = scoreType
		score = form[t+"_score"].value
		comment = form[t+"_comment"].value
		# strip to ASCII
		comment = filter(lambda x: x in string.printable, comment)
		
		
		# escape for LaTeX
		# take care of backslash (first), then tilde and caret
		comment = comment.replace("\\","\\textbackslash ")
		comment = comment.replace("~","\\textasciitilde ")
		comment = comment.replace("^","\\textasciicircum ")

		latexEscape="&%$#_{}"
		newComment = ""
		for char in str(comment):
			if char not in latexEscape:
				newComment+=char
			else:
				newComment+="\\"+char
		comment = newComment		
		
		outputText = outputText.replace("<"+t+"-score>",score)
		outputText = outputText.replace("<"+t+"-comments>",comment)

	return outputText	
	

form=cgi.FieldStorage()
keys=form.keys()

# make folder for today if we haven't already
t=datetime.datetime.now()
month=str(t.month)
if len(month)==1:
	month="0"+month

day = str(t.day)
if len(day)==1:
	day="0"+day
	
today=str(t.year)+"-"+month+"-"+day
today_folder=pres_folder+today+"/"

if not os.path.exists(today_folder):
	os.makedirs(today_folder)

# create a text file called team_evaluator_date
team = form['TeamPresenting'].value

evaluator=form['Evaluator'].value

filename=today_folder+team+"_"+evaluator.replace(" ", "_")+"_"+today+".tex"

# open the latex template file
with open(latexTemplate,"r") as templateFile:
	outputText = ''.join(templateFile.readlines())

# populate the output file with details of the evaluation
outputText = outputText.replace("<team-name>",team.replace("_"," "))
outputText = outputText.replace("<date>",today)
outputText = outputText.replace("<evaluator>",evaluator)

outputText = collateScores(outputText,form)

with open(filename,"w") as outputFile:
	outputFile.write(outputText)

sys.stdout.write("Content-Type: text/html")
sys.stdout.write("\n")
sys.stdout.write("\n")
sys.stdout.write("Submitted Form!\n")


