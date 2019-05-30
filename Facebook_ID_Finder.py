# -*- coding: utf-8 -*-
import re, argparse, sys, json, datetime, urllib.parse
from  requests_html import HTMLSession

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--uid" , help="Input user's UID.", dest="uid")
parser.add_argument("-f", "--file", help="File contain UIDs in Json format.", metavar="File Path", dest="user_file")
parser.add_argument("-t", "--target", help= "Get UID from target URL.", metavar="URL", dest="target")
args = parser.parse_args()

time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

ERROR = False

def Id2NameError(uid):
	session = HTMLSession()
	url = "https://www.facebook.com/profile.php?id={}".format(uid)
	result = session.get(url)
	result.html.render()

	timeline = result.html.find("span#fb-timeline-cover-name", first=True)
	if timeline:
		username = timeline.text
		userpage = list(timeline.links)[0]
		print("\nuid      = {}\nusername = {}\nURL      = {}".format(uid, username, userpage))
	else:
		timeline = result.html.find("#seo_h1_tag", first=True)
		if timeline:
			username = timeline.text
			userpage = list(timeline.links)[0]
			print("\nuid      = {}\nusername = {}\nURL      = {}".format(uid, username, userpage))
		else:
			username = uid
			userpage = url
			print("Error\nusername = {}\nURL      = {}".format(username, userpage))
			ERROR = True

	if args.user_file:
		with open("{}_fb.txt".format(time), 'a+') as f:  
			if ERROR:
				f.write("\nERROR\nuid      = {}\nusername = {}\nURL      = {}\n".format(uid, username, userpage))				
				ERROR = False
			else:
				f.write("\nuid      = {}\nusername = {}\nURL      = {}\n".format(uid, username, userpage))
def Id2Name(uid):
	session = HTMLSession()
	url = "https://www.facebook.com/profile.php?id={}".format(uid)
	result = session.get(url)
	try:
		redirect = result.html.search("window.location.replace(\"{}\")")[0]
	except:
		if "你點擊進來的連結可能已失效，或頁面可能已被移除" in result.html.html:
			username = uid
			userpage = url 
			print("Error:你點擊進來的連結可能已失效，或頁面可能已被移除\nusername = {}\nURL      = {}".format(username, userpage))
			if args.user_file:
				with open("{}_fb.txt".format(time), 'a+') as f:  
					f.write("\nERROR:你點擊進來的連結可能已失效，或頁面可能已被移除\nuid      = {}\nusername = {}\nURL      = {}\n".format(uid, username, userpage))				
		else:
			Id2NameError(uid)
		return	
	userpage = redirect.replace('\\','')
	result = session.get(userpage)	
	
	timeline = result.html.find("span#fb-timeline-cover-name", first=True)
	if timeline:
		username = timeline.text
		print("\nuid      = {}\nusername = {}\nURL      = {}".format(uid, username, userpage))
	else:
		timeline = result.html.find("#pageTitle", first=True)
		if timeline:
			username = timeline.text.split(' - 首頁 | Facebook')[0]
			print("\nuid      = {}\nusername = {}\nURL      = {}".format(uid, username, userpage))
		else:
			Id2NameError(uid)
			return	
	if args.user_file:
		with open("{}_fb.txt".format(time), 'a+') as f:  
			f.write("\nuid      = {}\nusername = {}\nURL      = {}\n".format(uid, username, userpage))

if args.target:
	session = HTMLSession()
	result = session.get(" https://www.facebook.com/jeff.hein.71")
	if result:
		profile_id = result.html.search("\"fb://profile/{}\"")[0]
		if not profile_id:
			profile_id = result.html.search("page_id={}\"")[0]
		print("uid = {}".format(profile_id))
	else:
	    	print('The target is invalid page.')

elif args.uid:
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


