import requests,lxml.html as lh,re,os,subprocess,json,sys,time
def wait_for_internet():
    print ('Waiting for internet..')
    # while True:
    #     p = subprocess.Popen("ping -c 1 8.8.8.8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True,
    #                          executable="/bin/bash")
    #     output = p.stdout.read()
    #     if output.find("100% packet loss") == -1 and output.find("connect: Network is unreachable") == -1:
    #         return
    #     else:
    #         sys.stdout.write("..")
    #         sys.stdout.flush()
            # time.sleep(2)
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
                print "\r-------------------------------Completed----------------------------------"
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
wait_for_internet()
class justdubbed(object):
	
	def __init__(self, link,startfrom=0):
		super(justdubbed, self).__init__()
		self.s_name=link.split("/")[-2]
		print self.s_name
		self.justdubbedlevel1(link,startfrom=startfrom)
	def justdubbedlevel1(self,link,try1=1,startfrom=0):
		if try1>3:
			print "error"
			return
		try:
			raw_data=requests.get(link)
		except Exception, e:
			print "justdubbedlevel1"+str(e)
			wait_for_internet()
			justdubbedlevel1(link,try1+1,startfrom)
		# 	return

		doc = lh.fromstring(raw_data.text)
		Episold_Links=doc.xpath('//ul[@id="archive-results"]/li/a/@href')
		Episold_Names=doc.xpath('//ul[@id="archive-results"]/li/a/text()')
		print "No Of Episold:",str(len(Episold_Links))
		self.justdubbedlevel2inter(Episold_Links,Episold_Names,startfrom)

	def justdubbedlevel2inter(self,Episold_Links,Episold_Names,startfrom=0):
		for epl in Episold_Links:
			if int(Episold_Names[Episold_Links.index(epl)].split(" ")[-1])>=startfrom:
				try:
					self.justdubbedlevel2(epl,Episold_Names[Episold_Links.index(epl)])
				except ValueError,e:
					pass

	def justdubbedlevel2(self,Episold_Link,Episold_Name,try1=1):
		if try1>3:
			print error
			return
		try:
			raw_data=requests.get(Episold_Link)
		except Exception, e:
			print "justdubbedlevel2"+str(e)
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
		if try1>3:
			print "error"
			return
		print Episold_Name +"\n\n"
		try:
			a = requests.get(Embeded_Link)
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', a.text)
			for i in urls:
				if i.find(".mp4") != -1:
					urls = i
					break
			print urls
			os.system("mkdir -p /home/manoj/Downloads/justdubbed/" + self.s_name + "/")
			namel = "/home/manoj/Downloads/justdubbed/" + self.s_name +"/"+Episold_Name + ".mp4"
			out = Run_process('wget  -c -T 10 -O "' + namel + '" "' + urls[:-2]+'"',Episold_Name)
			if out.find("failed:")!=-1 or out.find("unable to resolve host address")!=-1:
				raise Exception("wget error")
		except Exception,e:
			print "justdubbedlevel3"+str(e)
			wait_for_internet()
			self.justdubbedlevel3(Embeded_Link,Episold_Name,try1+1)
# justdubbed("http://www.justanimedubbed.tv/watch/assassination-classroom/")
# justdubbed("http://www.justanimedubbed.tv/watch/steinsgate/")
# justdubbed("http://www.justanimedubbed.tv/watch/sword-art-online/")
# justdubbed("http://www.justanimedubbed.tv/watch/sword-art-online-ii/")
# justdubbed("http://www.justanimedubbed.tv/watch/avatar-the-last-airbender/")
# justdubbed("http://www.justanimedubbed.tv/watch/avatar-the-legend-of-korra/")
# justdubbed("http://www.justanimedubbed.tv/watch/inuyasha/")
# justdubbed("http://www.justanimedubbed.tv/watch/fullmetal-alchemist-brotherhood/")
# justdubbed("http://www.justanimedubbed.tv/watch/blue-exorcist/")
# justdubbed("http://www.justanimedubbed.tv/watch/megas-xlr/")
justdubbed("http://www.justanimedubbed.tv/watch/fairy-tail/",200)
justdubbed("http://www.justanimedubbed.tv/watch/magical-warfare/")
justdubbed("http://www.justanimedubbed.tv/watch/infinite-stratos/")
justdubbed("http://www.justanimedubbed.tv/watch/infinite-stratos-2/")
justdubbed("http://www.justanimedubbed.tv/watch/angel-beats/")
justdubbed("http://www.justanimedubbed.tv/watch/shakugan-no-shana/")
justdubbed("http://www.justanimedubbed.tv/watch/avenger/")

# os.system("poweroff")