# -*- coding: utf-8 -*-
import re, argparse, sys, json, datetime, urllib.parse
from  requests_html import HTMLSession

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--uid" , help="Input user's UID.", dest="uid")
parser.add_argument("-f", "--file", help="File contain UIDs in Json format.", metavar="File Path", dest="user_file")
args = parser.parse_args()

time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def Id2Name(uid):
	session = HTMLSession()
	url = "https://twitter.com/{}".format(uid)
	result = session.get(url)
	userpage = url
	timeline = result.html.find("title", first=True)
	if timeline:
		username = timeline.text.split(' | Twitter')[0]
		print("\nuid      = {}\nusername = {}\nURL      = {}".format(uid, username, userpage))
		
	if args.user_file:
		with open("{}_tw.txt".format(time), 'a+') as f:  
			f.write("\nuid      = {}\nusername = {}\nURL      = {}".format(uid, username, userpage))


if args.uid:
	Id2Name(args.uid)	
elif args.user_file:
	with open(args.user_file) as json_file:  
		data = json.load(json_file)
	print("Total {} data.\n".format(len(data)))
	for ids in data:
		Id2Name(ids)
	print("Total {} data.\n".format(len(data)))	
else:
	parser.print_help()

