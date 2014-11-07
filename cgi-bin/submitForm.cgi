#!/usr/bin/env python

import cgi,sys,os
import cgitb
import uuid
import time,datetime
import json

pres_folder = "../presentations/"

cgitb.enable()

def ascii_horiz_line(f,num,newline=True):
	f.write("+")
	for i in range(num):
		f.write("-")
	if newline: f.write("+\n")
	
def ascii_table_line(f):
	ascii_horiz_line(f,15,False)
	ascii_horiz_line(f,7,False)
	ascii_horiz_line(f,60)
	
def print_comment(comment):
	# break comment down into 40-character pieces, but by words
	current_char = 0
	comment_left = comment
	
	while len(comment_left) > 0:
		partial_comment = comment_left[:40]
		comment_left = comment_left[40:]
		if len(partial_comment)==40:
			# keep looking until we have a space or the line ends
			# or we get to 60, in which case we just stop
			
	
		# now get the rest of the word
		while 
	
def collateScores(f,form):
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
		ascii_table_line(f)
		t,desc = scoreType
		score = form[t+"_score"].value
		comment = form[t+"_comment"].value
		
		f.write("| "+desc+"\t")
		f.write("|   "+score+"\t")
		f.write("| "+comment+"\n")
		
		# special cases (wrap)
		if t == "time":
			f.write("| Management    |\t|\n")
		if t == "realism":
			f.write("| Honest Status |\t|\n")
		if t == "audience":
			f.write("| Engagement    |\t|\n")
	ascii_table_line(f)
	

form=cgi.FieldStorage()
keys=form.keys()

# make folder for today if we haven't already
t=datetime.datetime.now()
today=str(t.year)+"-"+str(t.month)+"-"+str(t.day)
today_folder=pres_folder+today+"/"

if not os.path.exists(today_folder):
	os.makedirs(today_folder)

# create a text file called team_evaluator_date
team = form['TeamPresenting'].value
evaluator=form['Evaluator'].value

filename=today_folder+team+"_"+evaluator.replace(" ", "_")+"_"+today

# populate the text file with details of the evaluation
with open(filename,"w") as f:
	ascii_horiz_line(f,84)
	f.write("Team Name: "+team+"\n")
	f.write("Evaluator: "+evaluator+"\n")
	f.write("Presentation Date: "+today+"\n")
	ascii_table_line(f)
	f.write("| Category\t| Score\t| Comments\n")
	collateScores(f,form)
	

sys.stdout.write("Content-Type: text/html")
sys.stdout.write("\n")
sys.stdout.write("\n")
sys.stdout.write("Submitted Form!\n")
for key in keys:
	print key,":",form[key].value

