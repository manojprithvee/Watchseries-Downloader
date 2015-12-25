import requests,lxml.html as lh,re,os,subprocess,json,sys,time
def wait_for_internet():
    print ('Waiting for internet..')
    while True:
        p = subprocess.Popen("ping -c 1 8.8.8.8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True,
                             executable="/bin/bash")
        output = p.stdout.read()
        if output.find("100% packet loss") == -1 and output.find("connect: Network is unreachable") == -1:
            return
        else:
            sys.stdout.write("..")
            sys.stdout.flush()
            time.sleep(2)
wait_for_internet()
def notify(title1,message,try1=1,pri=0):
	if try1>=4:
		print "4 Retries failed"
		return
	try:
		a=requests.post('https://api.parse.com/1/push', data=json.dumps({"where": {"deviceType": "android"},"data": {"alert": message,"title":title1,"flag":""}}), headers={"X-Parse-Application-Id": "fMB6piQyYMpDbCnkJFrlfPZVS5nihQfADGqycvTH","X-Parse-REST-API-Key": "jiBr1uM5ip7oSYzwNYlL9QzI6eM62xfKxR3y5u3b","Content-Type": "application/json"})
	except Exception, e:
		print str(e)
		wait_for_internet()

		notify(title1,message,try1+1)
class justdubbed(object):
	
	def __init__(self, link):
		super(justdubbed, self).__init__()
		self.s_name=link.split("/")[-2]
		notify("JustDubbedAnime Downloader","Started Downloading "+self.s_name)
		self.justdubbedlevel1(link)
	def __del__(self):
		notify("JustDubbedAnime Downloader","Downloading Completed"+self.s_name)
	def justdubbedlevel1(self,link,try1=1):
		if try1>3:
			print error
		try:
			raw_data=requests.get(link)
		except Exception, e:
			print str(e)
			wait_for_internet()
			justdubbedlevel1(link,try1+1)
			return
		doc = lh.fromstring(raw_data.text)
		Episold_Links=doc.xpath('//ul[@id="archive-results"]/li/a/@href')
		Episold_Names=doc.xpath('//ul[@id="archive-results"]/li/a/text()')
		self.justdubbedlevel2inter(Episold_Links,Episold_Names)

	def justdubbedlevel2inter(self,Episold_Links,Episold_Names):
		for epl in Episold_Links:
			self.justdubbedlevel2(epl,Episold_Names[Episold_Links.index(epl)])


	def justdubbedlevel2(self,Episold_Link,Episold_Name,try1=1):
		if try1>3:
			print error
		try:
			raw_data=requests.get(Episold_Link)
		except Exception, e:
			print str(e)
			wait_for_internet()
			self.justdubbedlevel2(Episold_Link,Episold_Name,try1+1)
			return
		doc = lh.fromstring(raw_data.text)
		Embeded_Links=doc.xpath('//iframe/@src')
		temp=[]
		for i in Embeded_Links:
			if i.find("embed.php")!=-1:
				temp.append(i)
		Embeded_Links=temp
		self.justdubbedlevel3(Embeded_Links[0],Episold_Name)

	def justdubbedlevel3(self,Embeded_Link,Episold_Name,try1=1):
		print Episold_Name +"\n\n"
		try:
			a = requests.get(Embeded_Link)
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', a.text)
		except Exception,e:
			print str(e)
			wait_for_internet()
			justdubbedlevel3(self,Embeded_Link,Episold_Name,try1+1)
		for i in urls:
			if i.find(".mp4") != -1:
				urls = i
				break
		os.system("mkdir -p /home/manoj/Downloads/justdubbed/" + self.s_name + "/")
		namel = "/home/manoj/Downloads/justdubbed/" + self.s_name +"/"+Episold_Name + ".mp4"
		out = Run_process('wget  -c -T 10 -O "' + namel + '" "' + urls+'"',Episold_Name)

def Run_process(exe,Episold_Name):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, executable="/bin/bash")
    final = ""
    while True:
        retcode = p.poll()  # returns None while subprocess is running
        out = p.stdout.readline()
        out = out.replace(".......... ", "").replace(",......... ", "").replace(",,........ ", "").replace(
            ",,,....... ", "").replace(",,,,...... ", "").replace(",,,,,..... ", "").replace(",,,,,,.... ", "").replace(
            ",,,,,,,... ", "").replace(",,,,,,,,.. ", "").replace(",,,,,,,,,. ", "").replace(",,,,,,,,,, ", "")
        temp = out
        if len(temp) > 30:
            if out.find("     100%")!=-1:
                print "-------------------------------Completed----------------------------------"
                notify("JustDubbedAnime Downloader","Completed Downloading "+Episold_Name)
            else:
                print temp,
        if len(temp) < 30:
            if temp.find("skipping") == -1:
                a = out.strip().split(" ")
                if a != [""]:
                    a = [x for x in a if x != ""]
                    try:
                    	print("\r\033[K\033[07m" + "Downloaded: " + a[0] + "B Completed: " + a[1] + " Speed: " + a[2] + "B\s" + " Time Remaining: " + a[3] + "\033[0m "),
                    except:
                    	pass
        final = final + out
        if retcode is not None:
            return final	
justdubbed("http://www.justanimedubbed.tv/watch/rurouni-kenshin/")

