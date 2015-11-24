import requests,re,os,base64,subprocess,time,sys,notify2,json,atexit
import lxml.html as lh
FAIL = '\033[91m'
ENDC = '\033[0m'
notify2.init('watchseries downloader')
pkl_file = open('data.pkl', 'rb')
data = json.load(pkl_file)

def onexit():
	print "manoj"
	print type(data)
	output = open('data.pkl', 'wb')
	json.dump(data, output)
	output.close()
atexit.register(onexit)

def wait_for_internet():
	print ('Waiting for internet..' )
	while True:
		p = subprocess.Popen("ping -c 1 8.8.8.8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,executable="/bin/bash")
		output=p.stdout.read()
		if output.find("100% packet loss")==-1 and output.find("connect: Network is unreachable")==-1:
			return
		else:
			sys.stdout.write("..")
			sys.stdout.flush()
			time.sleep(2)
def runProcess(exe):
	p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,executable="/bin/bash")    
	final=""
	while(True):
		retcode = p.poll() #returns None while subprocess is running
		out=p.stdout.readline()
		out=out.replace(".......... ","")
		temp=out
		#
		# print len(temp)
		print out,
		final=final+out
		if(retcode is not None):
			return final

def gorillavia(link,name,season,episold,s_name):
	# try:
	if link.find("gorillavid.in")==-1:
		print FAIL + "This has no gorillavid Links" + ENDC
	else:
		a=requests.get(link,headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Moto G Build/LMY48Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36","Upgrade-Insecure-Requests":  1})
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', a.text)
		for i in urls:
			if i.find(".mp4")!=-1:
				urls=i
				break
		a=""
		os.system("mkdir -p /home/manoj/Downloads/watchseries/"+s_name+"/Season-"+str(season))
		namel="/home/manoj/Downloads/watchseries/"+s_name+"/Season-"+str(season)+"/"+s_name+"_S"+str(season)+"E"+str(episold)+"-"+name+".mp4"
		out=runProcess('wget  -c -O "'+namel+'" '+urls)
		data[s_name]["last_downloaded"]=(season,episold)
		if out.find("The file is already fully retrieved")==-1:
			n = notify2.Notification("File Downloaded:",namel.split("/")[-1],"notification-network-ethernet-connected")
			n.show()
		print data
	# except Exception, e:
	# 	print FAIL + str(e) + ENDC
	# 	wait_for_internet()
	# 	gorillavia(link,name,season,episold,s_name)
	# 	return
	


def leve1(link,i,j,s_name):
	try:
		a=requests.get(link)
	except Exception, e:
		print FAIL + str(e)+ ENDC
		wait_for_internet()
		leve1(link,i,j,s_name)
		return
	html=a.text.encode('ascii', 'ignore').decode('ascii')
	doc = lh.fromstring(a.text)
	final=doc.xpath('//*[2]/td[2]/a/@href')
	#print link
	name=doc.xpath("//title/text()")[0]
	name=name.split(" - ")[1]
	gorillavia(base64.b64decode(final[0].split("=")[1]),name,i,j,s_name)
def watchseries(link):
	s_name=link.split("/")[-1]
	epview=[]
	if s_name not in data:
		try:
			a=requests.get(link)
		except Exception, e:
			print FAIL + str(e) + ENDC
			wait_for_internet()
			watchseries(link)
			return
		html=a.text.encode('ascii', 'ignore').decode('ascii')
		doc = lh.fromstring(a.text)
		left=doc.xpath('//div[@id="left"]/div/ul/li/a/@href')
		right=doc.xpath('//div[@id="right"]/div/ul/li/a/@href')
		epview=right+left
		data[s_name]=dict()
		data[s_name]["episold_list"]=list(epview)
	else:
		epview=data[s_name]["episold_list"]
	season=0
	episold=0
	if "last_downloaded" in data[s_name]:
		season,episold=data[s_name]['last_downloaded']
	for i in range(50):
		for j in range(200):
			for x in epview:
				if i>=season and j>episold:
					if x.find("s"+str(i)+"_e"+str(j)+".html")!=-1:
						print ("s"+str(i)+"_e"+str(j))
						leve1("http://thewatchseries.to"+x,i,j,s_name)
	





def main():
	pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
	a=raw_input("enter the watchseries.to Link:")
	if pattern.match(a):
		if a.find("watchseries.to")!=-1:
			if a.find("/episode/")!=-1 and len(a.split("/"))==5:
				b=raw_input("enter the season number:")
				c=raw_input("enter the episode number:")
				d=raw_input("enter the episode name:")
				leve1(a,b,c,d)
			elif a.find("/serie/")!=-1 and len(a.split("/"))==5:
				watchseries(a)
			else:
				print "enter a url of a series or a episode"
		else:
			print "enter a watchseries.to link"
	else:
		print "enter a link "



#gorillavia("http://gorillavid.in/ntrjh7twzrf3")
#watchseries("http://thewatchseries.to/serie/avengers_assemble")
#watchseries("http://thewatchseries.to/serie/true_blood")
main()
#os.system("poweroff")