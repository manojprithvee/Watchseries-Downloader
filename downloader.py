# TODO add pause button
'''
options 
-reverse to start from latest episold
-p to poweroff after download is Completed
-l <number> limit the download in kb
'''
import requests, re, os, base64, subprocess, time, sys, notify2, json, atexit,threading
from pushover import init,Client
import lxml.html as lh
FAIL = '\033[91m'
ENDC = '\033[0m'
notify2.init('watchseries downloader')
try:
    pkl_file = open('data.json', 'rb')
    data = json.load(pkl_file)
except:
    data={}
gorillavialist = list()

def onexit():
    print "saving status.."
    output = open('data.json', 'wb')
    json.dump(data, output,indent=4)
    os.system("setterm -cursor on")
    os.system("stty echo")
    output.close()
    


atexit.register(onexit)

def notify(title1,message,try1,pri=0):
	if try1>=4:
		print "4 Retries failed"
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
		notify(title1,message,try1+1)

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





def Run_process(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, executable="/bin/bash")
    final = ""
    while True:
        retcode = p.poll()  # returns None while subprocess is running
        out = p.stdout.readline()
        out = out.replace(".......... ", "").replace(",......... ", "").replace(",,........ ", "").replace(
            ",,,....... ", "").replace(",,,,...... ", "").replace(",,,,,..... ", "").replace(",,,,,,.... ", "").replace(
            ",,,,,,,... ", "").replace(",,,,,,,,.. ", "").replace(",,,,,,,,,. ", "").replace(",,,,,,,,,, ", "")
        temp = out
        os.system("setterm -cursor off && stty -echo")
        if len(temp) > 30:
            if out.find("     100%")!=-1:
                print "-------------------------------Completed----------------------------------"
            else:
                print temp,
        if len(temp) < 30:
            if temp.find("skipping") == -1:
                a = out.strip().split(" ")
                if a != [""]:
                    a = [x for x in a if x != ""]
                    print("\033[K\033[07m" + "Downloaded: " + a[0] + "B Completed: " + a[1] + " Speed: " + a[
                        2] + "B\s" + " Time Remaining: " + a[3] + "\033[0m \r"),

        final = final + out
        if retcode is not None:
            os.system("setterm -cursor on && stty echo")
            return final


def gorillavia(link, name, season, episold, s_name,try1):
    print "S_" + str(season) + "E_" + str(episold)
    print "try "+str(try1)
    try:
        if link.find("gorillavid.in") == -1:
            print FAIL + "This has no gorillavid Links" + ENDC
        elif(try1==4):
            print FAIL + "tryed 3 time and failed" + ENDC
            return
        else:
            a = requests.get(link, headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Moto G Build/LMY48Y) AppleWebKit/537.36 (KHTML, like \
                Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36",
                "Upgrade-Insecure-Requests": 1})
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', a.text)
            for i in urls:
                if i.find(".mp4") != -1:
                    urls = i
                    break
            os.system("mkdir -p /home/manoj/Downloads/watchseries/" + s_name + "/Season-" + str(season))
            namel = "/home/manoj/Downloads/watchseries/" + s_name + "/Season-" + str(
                season) + "/" + s_name + "_S" + str(season) + "E" + str(episold) + "-" + name + ".mp4"
            if "-l" in sys.argv:
                try:
                    print "speed"
                    speed=int(sys.argv[sys.argv.index("-l")+1])
                    out = Run_process('wget  -c --limit-rate='+str(speed)+'k -O "' + namel + '" ' + urls)
                except Exception, e:
                    print FAIL + str(e) + ENDC
                    print "enter a number for speed"
                    os._exit(0)
            else:
                out = Run_process('wget  -c -O "' + namel + '" ' + urls)
            data[s_name]["last_downloaded"] = (season, episold)
            if out.find("416 Requested Range Not Satisfiable") == -1:
                n = notify2.Notification("File Downloaded:", namel.split("/")[-1],
                                         "notification-network-ethernet-connected")
                n.show()
                notify("WS Downloader ("+str(data[s_name]["episold_list"].index([link, name, season, episold, s_name])+1)+"/"+str(len(data[s_name]["episold_list"]))+")","File Downloaded: "+namel.split("/")[-1],1)
            if out.find("failed:")!=-1:
                gorillavia(link, name, season, episold, s_name,try1+1)
                return
    except Exception, e:
        print FAIL + str(e) + ENDC
        global client
        if try1==1:
            notify("WS Downloader S_" + str(season) + "E_" + str(episold),str(e),1,1)
        wait_for_internet()
        gorillavia(link,name,season,episold,s_name,try1+1)
        return


def leve1(link, i, j, s_name,try1):
    print ("s" + str(i) + "_e" + str(j))
    if(try1==4):
        print FAIL + "tryed 3 time and failed" + ENDC
        return
    try:
        a = requests.get(link,timeout=10)
    except Exception, e:
        print FAIL + str(e) + ENDC
        wait_for_internet()
        leve1(link,i,j,s_name,try1+1)
        return
    doc = lh.fromstring(a.text)
    final = doc.xpath('//*[2]/td[2]/a/@href')
    # print link
    name = doc.xpath("//title/text()")[0]
    name = name.split(" - ")[1]
    if final!=[]:
        gorillavialist.append([base64.b64decode(final[0].replace("/cale.html?r=", "")[:56]), name, i, j, s_name])
        time.sleep(5)
    else:
        print "no links found"


def leve1_epi(link,i,j,s_name,try1):
    if(try1==4):
        print FAIL + "tryed 3 time and failed" + ENDC
        return
    try:
        a=requests.get(link)
    except Exception, e:
        print FAIL + str(e)+ ENDC
        wait_for_internet()
        leve1_epi(link,i,j,s_name,try1+1)
        return
    html=a.text.encode('ascii', 'ignore').decode('ascii')
    doc = lh.fromstring(a.text)
    final=doc.xpath('//*[2]/td[2]/a/@href')
    #print link
    name=doc.xpath("//title/text()")[0]
    name=name.split(" - ")[1]
    gorillavia(base64.b64decode(final[0].replace("/cale.html?r=","")[:56]),name,i,j,s_name,1)

def rundownload(s_name):
    data[s_name]["episold_list"] = list(gorillavialist)
    season = -1
    episold = -1
    if "--reverse" in sys.arvg:
        gorillavialist=gorillavialist[::-1]
    if "last_downloaded" in data[s_name]:
        season, episold = data[s_name]['last_downloaded']
    for i in gorillavialist:
        if i[2] >= season and i[3] > episold:
            gorillavia(i[0], i[1], i[2], i[3], i[4],1)
            output = open('data.json', 'wb')
            json.dump(data, output,indent=4)
            season = -1
            episold = -1


def watchseries(link):
    s_name = link.split("/")[-1]
    print s_name
    if s_name not in data:
            datamining(link,s_name)
            notify("WS Downloader","Datamining Completeed for "+s_name,1)
            rundownload(s_name)
            notify("WS Downloader",s_name+" Completed Downloading",1)
            gorillavialist=list()

    else:
        if int(round(time.time() * 1000))-data[s_name]["lastupdate"]>864000000:
            print int(round(time.time() * 1000))-data[s_name]["lastupdate"]
            datamining(link,s_name)
            rundownload(s_name)
            notify("WS Downloader",s_name+" Completed Downloading",1)
            gorillavialist=list()
        else:
            notify("WS Downloader","Datamining Completeed for "+s_name,1)
            print "previous data found and starting resuming"
            global gorillavialist
            gorillavialist = data[s_name]["episold_list"]
            rundownload(s_name)
            notify("WS Downloader",s_name+" Completed Downloading",1)
            gorillavialist=list()

def datamining(link,s_name):
    try:
        a = requests.get(link)
    except Exception, e:
        print FAIL + str(e) + ENDC
        wait_for_internet()
        watchseries(link)
        return
    doc = lh.fromstring(a.text)
    epview = doc.xpath('//meta[@itemprop="url"]/@content')
    for i in range(50):
        for j in range(200):
            for x in epview:
                if x.find("s" + str(i) + "_e" + str(j) + ".html") != -1:
                    leve1("http://thewatchseries.to" + x, i, j, s_name,1)
    notify("WS Downloader","Datamining Completeed for "+s_name,1)
    data[s_name] = {}
    data[s_name]["lastupdate"]=int(round(time.time() * 1000))

def main():
    pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    a = raw_input("enter the watchseries.to Link:")
    if pattern.match(a):
        if a.find("watchseries.to") != -1:
            if a.find("/episode/") != -1 and len(a.split("/")) == 5:
                b = raw_input("enter the season number:")
                c = raw_input("enter the episode number:")
                d = raw_input("enter the episode name:")
                leve1_epi(a, b, c, d,1)
            elif a.find("/serie/") != -1 and len(a.split("/")) == 5:
                watchseries(a)
            else:
                print "enter a url of a series or a episode"
        else:
            print "enter a watchseries.to link"
    else:
        print "enter a link "

# watchseries("http://thewatchseries.to/serie/true_blood")
watchseries("http://thewatchseries.to/serie/the_vampire_diaries")
watchseries("http://thewatchseries.to/serie/The_Originals")
if "-p" in sys.argv:
        os.system("sudo poweroff")
# watchseries("http://thewatchseries.to/serie/daredevil")
# main()
