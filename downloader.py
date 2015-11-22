import requests,re,os,base64,subprocess,time,sys,notify2
import lxml.html as lh
FAIL = '\033[91m'
ENDC = '\033[0m'
notify2.init('watchseries downloader')
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

def gorillavia(link,name,season,episold,s_name):
	try:
		if link.find("gorillavid.in")==-1:
			print FAIL + "This has no gorillavid Links" + ENDC
		else:
			a=requests.get(link,headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Moto G Build/LMY48Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36","Upgrade-Insecure-Requests":  1})
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', a.text)
			print urls[10]
			os.system("mkdir -p /home/manoj/Downloads/watchseries/"+s_name+"/Season-"+str(season))
			name="/home/manoj/Downloads/watchseries/"+s_name+"/Season-"+str(season)+"/"+s_name+"_S"+str(season)+"E"+str(episold)+"-"+name+".mp4"
			os.system('wget -c -O "'+name+'" '+urls[10])
			n = notify2.Notification("File Downloaded:",name.split("/")[-1])
			n.show()
	except Exception, e:
		print FAIL + str(e) + ENDC
		wait_for_internet()
		gorillavia(link,name,season,episold,s_name)
		return
	


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
	try:
		gorillavia(base64.b64decode(final[0].split("=")[1]),name,i,j,s_name)
	except Exception, e:
		print FAIL+s_name+"-Season"+str(i)+"-Episode"+str(j)+"-"+name+" has no links"+ ENDC
def watchseries(link):
	s_name=link.split("/")[-1]
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
#-----soarting episold so first download first-----#
	for i in range(50):
		for j in range(200):
			for x in epview:
				if x.find("s"+str(i)+"_e"+str(j)+".html")!=-1:
					print ("s"+str(i)+"_e"+str(j))
					leve1("http://thewatchseries.to"+x,i,j,s_name)
					







#gorillavia("http://gorillavid.in/ntrjh7twzrf3")
watchseries("http://thewatchseries.to/serie/avengers_assemble")
#os.system("poweroff")