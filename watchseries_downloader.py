'''
options
-new to add new series to the list
-reverse to start from latest episold
-l <number> limit the download in kb
'''
import requests, re, os, base64, subprocess, time, sys, json, atexit,threading,getpass,lxml.html as lh,platform,traceback
Ostype=platform.system()
if Ostype!="Windows":
    if subprocess.call("type wget", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
        print "Install wget and try again"
FAIL = '\033[91m'
ENDC = '\033[0m'
data={}
flagnotin=1
gorillavialist = list()
notification_complete=""
filread=open("data.json","r")
s_names=json.loads(filread.read())

class allmyvideos:
    def __init__(self, links):
        self.linklist=list()
        temp = list()
        for i in links:
            if i.find("allmyvideos") != -1:
                temp.append(i);
        links = temp
        link720p = list()
        link360p = list()
        link480p = list()
        for i in links:
            id = i.split("/")[-1]
            data = {
                'op': 'download1',
                'usr_login': '',
                'id': id,
                'fname': '',
                'referer': 'http://thewatchseries.to/cale.html?r=aHR0cDovL2FsbG15dmlkZW9zLm5ldC9wdm01aTNmOGNwNXo=',
                'method_free': '1',
            }
            a = requests.post(i, data, headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Moto G Build/LMY48Y) AppleWebKit/\
                537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36",
                "Upgrade-Insecure-Requests": 1})
            x = re.findall('(?<="sources" : )[.\s{"\[a-z:/0-9?,}\]]*(?=,)', a.text)[0]
            x = json.loads(x)
            for j in x:
                if j["label"] == '360':
                    link360p.append(j["file"])
                if j["label"] == '480':
                    link480p.append(j["file"])
                if j["label"] == '720':
                    link720p.append(j["file"])
            self.linklist = link360p + link480p + link720p

    def getlinks(self):
        """

        :rtype: list
        """
        return self.linklist


class filehoot:
    def __init__(self, links):
        self.linklist=list()
        temp = list()
        for i in links:
            if i.find("filehoot") != -1:
                temp.append(i);
        links = temp
        for i in links:
            id = i.split("/")[-1].replace(".html", "")
            data = {
                'op': 'download1',
                'usr_login': '',
                'id': id,
                'fname': '',
                'referer': '',
                'method_free': 'Continue to watch your Video',
            }
            a = requests.post(i, data, headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Moto G Build/LMY48Y) AppleWebKit/\
                537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36",
                "Upgrade-Insecure-Requests": 1})
            urls = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", a.text)
            for i in urls:
                if i.find(".mp4") != -1:
                    self.linklist.append(i)
                    break

    def getlinks(self):
        """

        :rtype: list
        """
        return self.linklist


class openload:
    def __init__(self, links):
        self.linklist=list()
        temp = list()
        for i in links:
            if i.find("openload") != -1:
                temp.append(i);
        links = temp
        for i in links:
            i = i.replace("https://openload.co/f/", "https://1fgm8ru.oloadcdn.net/dl/l/lAWx2pOBVdU/")
            self.linklist.append(i)

    def getlinks(self):
        """

        :rtype: list
        """
        return self.linklist[::-1]


class streamin:
    def __init__(self, links):
        self.linklist = list()
        temp = list()
        for i in links:
            if i.find("streamin") != -1:
                temp.append(i);
        links = temp
        for i in links:
            s = requests.session()
            a = s.get(i)
            doc = lh.fromstring(a.text.encode("utf-8"))
            data = {
                'op': 'download1',
                'usr_login': '',
                'id': doc.xpath('//input[@name="id"]/@value')[0],
                'fname': doc.xpath('//input[@name="fname"]/@value')[0],
                'referer': doc.xpath('//input[@name="referer"]/@value')[0],
                'hash': doc.xpath('//input[@name="hash"]/@value')[0],
                'imhuman': doc.xpath('//input[@name="imhuman"]/@value')[0],
                'method_free': 'Continue to watch your Video'
            }
            time.sleep(4)
            a = s.post(i, data, headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Moto G Build/LMY48Y) AppleWebKit\
                /537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36",
                "Upgrade-Insecure-Requests": 1,
                "Cookie": "__cfduid=dd3f1044204f9cdeb7745e401237f93201457071209; lang=1;file_id=4105293; aff=80; ref_url=http%3A%2F%2Fthewatchseries.to%2Fcale.html%3Fr%3DaHR0cDovL3N0cmVhbWluLnRvL2Fma2I2ZjJqMGwzNA%3D%3D; __utmt=1;__utma=30906109.221046949.1457071212.1457071212.1457071212.1;__utmb=30906109.1.10.1457071212; __utmc=30906109; __utmz=30906109.1457071212.1.1.utmcsr=thewatchseries.to|utmccn=(referral)|utmcmd=referral|utmcct=/cale.html; __test;adk2_catfish=1%7CFri,%2004%20Mar%202016%2006:01:13%20GMT;FastPopSessionRequestNumber=1"})
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', a.text)
            for i in urls:
                if i.find(".mp4") != -1:
                    self.linklist.append(i);
                    break

    def getlinks(self):
        """

        :rtype: list
        """
        return self.linklist


class gorillavid:
    def __init__(self, links):
    	print ("\033[K\033[07mgetting Links \033[0m \r"),
        self.linklist = list()
        temp = list()
        for i in links:
            if i.find("http://gorillavid.in/") != -1 or i.find("daclips") != -1 or i.find("movpod") != -1:
                temp.append(i);
                if len(temp)>5:
                	break
        links = temp
        for i in links:
            a = requests.get(i, headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Moto G Build/LMY48Y)\
                 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36",
                "Upgrade-Insecure-Requests": 1})
            urls = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", a.text)
            for i in urls:
                if i.find(".mp4") != -1:
                    self.linklist.append(i)

    def getlinks(self):
        """

        :rtype: list
        """
        return self.linklist

def onexit():
    print "saving status.."
    if notification_complete!="":
        notify("WS Downloader - newly downloaded",notification_complete)

atexit.register(onexit)

def notify(title1,message,try1=1,pri=0):
    if try1>=4:
        print "4 Retries failed"
        return
    try:
        a=requests.post('https://api.parse.com/1/push', data=json.dumps({
       "where": {
         "deviceType": "android"
       },
       "data": {
         "alert": message,
         "title":title1,
         "flag":"watchseries"
       }
     }), headers={
       "X-Parse-Application-Id": "fMB6piQyYMpDbCnkJFrlfPZVS5nihQfADGqycvTH",
       "X-Parse-REST-API-Key": "jiBr1uM5ip7oSYzwNYlL9QzI6eM62xfKxR3y5u3b",
       "Content-Type": "application/json"
     })
    except:
        wait_for_internet()
        notify(title1,message,try1+1)

def wait_for_internet():
    waitcount=1
    while True:
        p = subprocess.Popen("ping -c 1 8.8.8.8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        output = p.stdout.read()
        if output.find("100% packet loss") == -1 and output.find("connect: Network is unreachable") == -1:
            return
        else:
            if waitcount==1:
                print 'Waiting for internet..',
                waitcount=0
            sys.stdout.write(".")
            sys.stdout.flush()

def Run_process(exe,namel,season, episold,s_name):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
    final = ""
    abc=0
    while True:
        retcode = p.poll()
        out = p.stdout.readline()
        out = out.replace(".......... ", "").replace(",......... ", "").replace(",,........ ", "").replace(
            ",,,....... ", "").replace(",,,,...... ", "").replace(",,,,,..... ", "").replace(",,,,,,.... ", "").replace(
            ",,,,,,,... ", "").replace(",,,,,,,,.. ", "").replace(",,,,,,,,,. ", "").replace(",,,,,,,,,, ", "").replace("..", "")
        temp = out
        global data
        if len(temp) > 30:
            print temp,
        if len(temp) < 30:
            if temp.find("skipping") == -1:
                a = out.strip().split(" ")
                if a != [""]:
                    a = [x for x in a if x != ""]
                    try:
	                    print("\033[K\033[07m" + "Downloaded: " + a[0] + "B Completed: " + a[1] + " Speed: " + a[
	                        2] + "B\s Time : " + a[3] +" episold: " + "S_" + str(season) + "E_" + str(episold) + "\033[0m \r"),
                    except:
        				pass
        final = final + out
        if abc==0 and final.find("100%")!=-1:
            abc=1
            global notification_complete
            print ("\033[K\033[07m" +"Completed "+s_name+" Season "+str(season)+" Episode "+str(episold)+ "\033[0m \r"),
            notification_complete=notification_complete+s_name +' Season '+str(season)+" Episold "+str(episold)+"\n"
        if abc==0 and final.find("416 Requested Range Not Satisfiable")!=-1:
            abc=1
            print ("\033[K\033[07m" +"Already Downloaded "+s_name+" Season "+str(season)+" Episode "+str(episold)+ "\033[0m \r"),
        if retcode is not None:
            return final

def wgethander(links, name, season, episold, s_name,try1):
    global s_names
    try:
        if(try1==11):
            print FAIL + "S_" + str(season) + "E_" + str(episold) +"\nTryed 10 Time And Failed" + ENDC
            return
        if try1>1:
            time.sleep(5)
        urls = gorillavid(links).getlinks()
        if len(urls) == 0:
            urls = allmyvideos(links).getlinks()
        if len(urls) == 0:
            urls = openload(links).getlinks()
        if len(urls) == 0:
            urls = filehoot(links).getlinks()
        if len(urls) == 0:
            urls = streamin(links).getlinks()

        if Ostype=="Windows":
            try:
                os.makedirs("C:\Users\\"+getpass.getuser()+"\Downloads\watchseries\\" + s_name + "\Season-" + str(season))
            except:
                pass
            namel = "C:\Users\\"+getpass.getuser()+"\Downloads\watchseries\\" + s_name + "\\Season-" + str(
            season) + "\\" + s_name + "_S" + str(season) + "E" + str(episold) + "-" + re.sub('[^-a-zA-Z0-9_.() ]+', '-', name) + ".mp4"
        elif Ostype=="Linux":
            try:
                os.makedirs("/home/"+getpass.getuser()+"/Downloads/watchseries/" + s_name + "/Season-" + str(season))
            except:
                pass
            namel = "/home/"+getpass.getuser()+"/Downloads/watchseries/" + s_name + "/Season-" + str(
            season) + "/" + s_name + "_S" + str(season) + "E" + str(episold) + "-" + re.sub('[^-a-zA-Z0-9_.() ]+', '-', name) + ".mp4"
        elif Ostype=="Darwin":
            try:
                os.makedirs("~/Downloads/watchseries/" + s_name + "/Season-" + str(season))
            except:
                pass
            namel="~/Downloads/watchseries/" + s_name + "/Season-" + str(
            season) + "/" + s_name + "_S" + str(season) + "E" + str(episold) + "-" + re.sub('[^-a-zA-Z0-9_.() ]+', '-', name) + ".mp4"
        if "-l" in sys.argv:
            try:
                
                speed=int(sys.argv[sys.argv.index("-l")+1])
                print "speed is "+str(speed)
                if Ostype=="Windows":
                    out = Run_process('wget.exe  -c --tries=3 --limit-rate='+str(speed)+'k -O "' + namel + '" ' + urls[0],namel,season, episold,s_name)
                else:
                    out = Run_process('wget  -c --tries=3 --limit-rate='+str(speed)+'k -O "' + namel + '" ' + urls[0],namel,season, episold,s_name)
                if out.find("100%")!=-1:
                    flagnotin=1
                    for j in s_names:	
                        if j[0]==s_name:
                        	if len(j)==1:
                        		j=j+[season,episold+1]
                        	else:
                                    j[1]=season
                                    j[2]=episold+1
                                    flagnotin=0
                    if flagnotin==1:
                        s_names=[[s_name,int(season),int(episold)]]+s_names

                    filwite=open("data.json","w")
                    filwite.write(json.dumps(s_names))
                    filwite.close()
                if out.find("failed:")!=-1 or out.find("ERROR 404")!=-1 or out.find("No data received.")!=-1:
					links.pop(0)
					wgethander(links, name, season, episold, s_name,try1+1)
            except Exception, e:
                print FAIL + "S_" + str(season) + "E_" + str(episold)+"\n" +str(traceback.print_exc()) + ENDC
                print "enter a number for speed"
                os._exit(0)
        else:
            if Ostype=="Windows":
                out = Run_process('wget.exe -c  --tries=3 -O "' +  namel + '" ' + urls[0],namel,season, episold,s_name)
            else:
                out = Run_process('wget  -c  --tries=3 -O "' + namel + '" ' + urls[0],namel,season, episold,s_name)
            if out.find("100%")!=-1:
                flagnotin=1
                for j in s_names:	
                    if j[0]==s_name:
                    	if len(j)==1:
                    		j=j+[season,episold+1]
                    	else:
                                j[1]=season
                                j[2]=episold+1
                                flagnotin=0
                if flagnotin==1:
                    s_names=[[s_name,int(season),int(episold)]]+s_names
                filwite=open("data.json","w")
                filwite.write(json.dumps(s_names))
                filwite.close()
            if out.find("failed:")!=-1 or out.find("ERROR 404")!=-1 or out.find("No data received.")!=-1:
				print links
				links.pop(0)
				wgethander(links, name, season, episold, s_name,try1+1)
    except Exception, e:
        links.pop(0)
        wgethander(links, name, season, episold, s_name,try1+1)

def leve1(link, i, j, s_name, try1):
    if (try1 == 11):
        print FAIL + "tryed 10 time and failed" + ENDC
        return
    if try1>1:
        time.sleep(5)
    print ("\033[K\033[07m" +"Data Mining progress.. S_"+str(i)+"E_"+str(j)+ "\033[0m \r"),
    try:
        a = requests.get(link, timeout=10)
    except Exception, e:
        wait_for_internet()
        leve1(link, i, j, s_name, try1 + 1)
        return
    doc = lh.fromstring(a.text)
    temp = list()
    final = re.findall('(?<=\/cale.html\?r=)\w+.*(?=" class)', a.text)
    for x in final:
        temp.append(base64.b64decode(x))
    final = temp
    # final = doc.xpath('//tr[2]/td[2]/a/@href')
    name = doc.xpath("//title/text()")[0]
    name = name.split(" - ")[1]
    if final != []:
        gorillavialist.append([final, name, i, j, s_name])
    else:
        pass

def leve1_epi(link, i, j, s_name, try1=1):
    if (try1 == 11):
        print FAIL + "tryed 10 time and failed" + ENDC
        return
    if try1>1:
        time.sleep(5)
    try:
        a = requests.get(link)
    except Exception, e:
        print FAIL + "S_" + str(i) + "E_" + str(j) + "\n" + str(e) + ENDC
        wait_for_internet()
        leve1_epi(link, i, j, s_name, try1 + 1)
        return
    doc = lh.fromstring(a.text)
    temp = list()
    final = re.findall('(?<=\/cale.html\?r=)\w+.*(?=" class)', a.text)
    for x in final:
        temp.append(base64.b64decode(x))
    final = temp
    # final = doc.xpath('//tr[2]/td[2]/a/@href')
    name = doc.xpath("//title/text()")[0]
    name = name.split(" - ")[1]
    wgethander(final, name, i, j, s_name, 1)

def rundownload(s_name):
    global gorillavialist
    data[s_name]["episold_list"] = list(gorillavialist)
    season = 1
    
    if "--reverse" in sys.argv:
        gorillavialist=gorillavialist[::-1]
    threads=list()
    for season in range(50):
        for episold in range(200):
            for i in gorillavialist:
                if i[2] == season and i[3] == episold:
                    print ("\033[K\033[07m" +"Starting "+s_name+" Season "+str(i[2])+" Episode "+str(i[3])+ "\033[0m \r"),
                    wgethander(i[0], i[1], i[2], i[3], i[4],1)
    gorillavialist=list()


def watchseries(link,start_season=0,start_episold=0,final_season=50000,final_episold=50000):
    wait_for_internet()
    s_name = link.split("/")[-1]
    print "\n"+s_name.replace("_"," ")
    datamining(link,s_name,start_season,start_episold,final_season,final_episold)
    rundownload(s_name)
    gorillavialist=list()

def datamining(link,s_name,start_season,start_episold,final_season,final_episold,try1=1):
    if (try1 == 11):
        print FAIL + "tryed 10 time and failed" + ENDC
        return
    if try1>1:
        time.sleep(5)
    try:
        a = requests.get("https://query.yahooapis.com/v1/public/yql?q=select * from html where url='"+link+"' and xpath='//meta[@itemprop=\"url\"]/@content'&format=json")
    except Exception, e:
        print FAIL + str(traceback.print_exc()) + ENDC
        wait_for_internet()
        datamining(link,s_name,start_season,start_episold,final_season,final_episold,try1+1)
        return
    rawjson=json.loads(a.text)
    epview=list()
    if rawjson['query']['results']==None:
    	print "Server down"
    for i in rawjson['query']['results']['meta']:
        epview.append(i['content'])
    threads=list()
    breaker=False
    for i in range(50):
        if breaker:
            break
        for j in range(200):
            if breaker:
                break
            for x in epview:
                if x.find("s" + str(i) + "_e" + str(j) + ".html") != -1:
                    if i >= start_season:
                        if j >= start_episold:
                            if i==final_season:
	                                if j>final_episold:
										print "manoj"
										breaker=True
										break

                            if breaker==False:
								if i>final_season:
									breaker=True
									break
								start_episold=0
								# print i,j
								# leve1("http://thewatchseries.to" + x, i, j, s_name,1)
								threads.append(threading.Thread(target=leve1,args=("http://thewatchseries.to" + x, i, j, s_name,1)))
            
        
                
    index=1
    sublist=list()
    for a in threads:
        if index%15==0:
            for i in sublist:
                i.join()
            sublist=list()
        a.start()
        sublist.append(a)
        index=index+1
    for i in sublist:
        i.join() 
    data[s_name] = {}

def main():
    pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    a = raw_input("enter the watchseries.to Link:")
    if pattern.match(a):
        if a.find("watchseries") != -1:
            wait_for_internet()
            if a.find("/episode/") != -1 and len(a.split("/")) == 5:
                b = re.findall("s\d+",a)[0].replace("s","")
                c = re.findall("e\d+",a)[0].replace("e","")
                d=a.split("/")[-1].replace("_s"+b+"_e"+c+".html","")
                print "Single Episode Downloading "+d+" Season "+b+" Episode "+c
                leve1_epi(a, b, c, d)
            elif a.find("/serie/") != -1 and len(a.split("/")) == 5:

                if raw_input("Do you want to start from the top (y or n)").lower()!="y":
                    watchseries(a,int(raw_input("enter the sesaon number")),int(raw_input("enter the Episold number")))
                else:
                    watchseries(a)
            else:
                print "enter a url of a series or a episode"
        else:
            print "enter a watchseries.to link"
    else:
        print "enter a link "
if __name__ == '__main__':
    print "\t+---------------------------+\n\t|  Watch Series Downloader  |\n\t|            By             |\n\t|      Spider  Studios      |\n\t+---------------------------+"
    if "-new" in sys.argv:
        main()
    else:
        threads=list()
        for i in s_names:
            if len(i)==3:
                watchseries("http://thewatchseries.to/serie/"+i[0],i[1],i[2])
            elif len(i)==1:
                watchseries("http://thewatchseries.to/serie/"+i[0])
            elif len(i)==4:
                watchseries("http://thewatchseries.to/serie/"+i[0],i[1],i[2],i[3])
            elif len(i)==5:
                watchseries("http://thewatchseries.to/serie/"+i[0],i[1],i[2],i[3],i[4])
            else:
                raise ValueError(i[0]+" -- watchseries-Need Exactly 1 or 3 or 4 Arguments given "+ len(i))
