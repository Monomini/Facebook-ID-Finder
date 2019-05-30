import re, argparse, sys, json, datetime, urllib.parse
from  requests_html import HTMLSession

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--uid" , help="Input user's UID.", dest="uid")
parser.add_argument("-f", "--file", help="File contain UIDs in Json format.", metavar="File Path", dest="user_file")
parser.add_argument("-t", "--target", help= "Get UID from target URL.", metavar="URL", dest="target")
args = parser.parse_args()

time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def Id2NameError(uid):
	session = HTMLSession()
	url = "https://www.facebook.com/profile.php?id={}".format(uid)
	result = session.get(url)
	result.html.render()

	timeline = result.html.find("span#fb-timeline-cover-name", first=True)
	if timeline:
		username = timeline.text
		userpage = list(timeline.links)[0]
		print("username = {}\nURL      = {}".format(username, userpage))
	else:
		timeline = result.html.find("#seo_h1_tag", first=True)
		if timeline:
			username = timeline.text
			userpage = list(timeline.links)[0]
			print("username = {}\nURL      = {}".format(username, userpage))
		else:
			username = uid
			print("Error\nusername = {}\nURL      = {}".format(username, userpage))

	if args.user_file:
		with open("{}_fb.txt".format(time), 'a+') as f:  
			f.write("\nusername = {}\nURL      = {}".format(username, userpage))
def Id2Name(uid):
	session = HTMLSession()
	url = "https://www.facebook.com/profile.php?id={}".format(uid)
	result = session.get(url)
	redirect = result.html.search("window.location.replace(\"{}\")")[0]
	userpage = redirect.replace('\\','')
	result = session.get(userpage)
	print(userpage)
	
	timeline = result.html.find("span#fb-timeline-cover-name", first=True)
	if timeline:
		username = timeline.text
		print("username = {}\nURL      = {}".format(username, userpage))
	else:
		timeline = result.html.find("#pageTitle", first=True)
		if timeline:
			username = timeline.text.split(' - 首頁 | Facebook')[0]
			print("username = {}\nURL      = {}".format(username, userpage))
		else:
			Id2NameError(uid)
			return	
	if args.user_file:
		with open("{}_fb.txt".format(time), 'a+') as f:  
			f.write("\nusername = {}\nURL      = {}".format(username, userpage))

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
	for ids in data:
		Id2Name(ids)
	
else:
	parser.print_help()


