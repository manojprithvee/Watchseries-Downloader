# TODO sys.arvg argument to limit download,send mobile notification
# TODO add pause button
import requests, re, os, base64, subprocess, time, sys, notify2, json, atexit
from pushover import init,Client
import lxml.html as lh
init("aa9MYCS3kvMkczTboARYzrGFXU2YWM")
client = Client("uxCwRsHcWuAnqJWpphtHWwYnpVMFHv")
FAIL = '\033[91m'
ENDC = '\033[0m'
notify2.init('watchseries downloader')
pkl_file = open('data.json', 'rb')
data = json.load(pkl_file)
gorillavialist = list()

def onexit():
    print "saving status.."
    output = open('data.json', 'wb')
    json.dump(data, output,indent=4)
    os.system("setterm -cursor on")
    os.system("stty echo")
    output.close()
    if "-p" in sys.argv:
        os.system("poweroff")


atexit.register(onexit)

def notify(title1,message,try1,pri=0):
	if try1>=4:
		print "4 Retries failed"
	try:
		global client
		client.send_message(message=message, title=title1,priority=pri)
	except:
		notify(title1,message,pri,try1+1)

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
            out = Run_process('wget  -c -O "' + namel + '" ' + urls)
            data[s_name]["last_downloaded"] = (season, episold)
            if out.find("416 Requested Range Not Satisfiable") == -1 or True:
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
    global data
    data[s_name]["episold_list"] = list(gorillavialist)
    season = -1
    episold = -1
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
            try:
                a = requests.get(link)
            except Exception, e:
                print FAIL + str(e) + ENDC
                wait_for_internet()
                watchseries(link)
                return
            doc = lh.fromstring(a.text)
            left = doc.xpath('//div[@id="left"]/div/ul/li/a/@href')
            right = doc.xpath('//div[@id="right"]/div/ul/li/a/@href')
            epview = right + left
            for i in range(50):
                for j in range(200):
                    for x in epview:
                        if x.find("s" + str(i) + "_e" + str(j) + ".html") != -1:
                            leve1("http://thewatchseries.to" + x, i, j, s_name,1)
            data[s_name] = {}
            data[s_name]["lastupdate"]=int(round(time.time() * 1000))
            rundownload(s_name)
    else:
        if int(round(time.time() * 1000))-data[s_name]["lastupdate"]>86400000:
            try:
                a = requests.get(link)
            except Exception, e:
                print FAIL + str(e) + ENDC
                wait_for_internet()
                watchseries(link)
                return
            doc = lh.fromstring(a.text)
            left = doc.xpath('//div[@id="left"]/div/ul/li/a/@href')
            right = doc.xpath('//div[@id="right"]/div/ul/li/a/@href')
            epview = right + left
            for i in range(50):
                for j in range(200):
                    for x in epview:
                        if x.find("s" + str(i) + "_e" + str(j) + ".html") != -1:
                            leve1("http://thewatchseries.to" + x, i, j, s_name,1)
            data[s_name] = {}
            data[s_name]["lastupdate"]=int(round(time.time() * 1000))
            rundownload(s_name)
        else:
            print "previous data found and starting resuming"
            global gorillavialist
            gorillavialist = data[s_name]["episold_list"]
            rundownload(s_name)
            gorillavialist=list()

def main():
    pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    a = raw_input("enter the watchseries.to Link:")
    if pattern.match(a):
        if a.find("watchseries.to") != -1:
            if a.find("/episode/") != -1 and len(a.split("/")) == 5:
                b = raw_input("enter the season number:")
                c = raw_input("enter the episode number:")
                d = raw_input("enter the episode name:")
                leve1_epi(a, b, c, d)
            elif a.find("/serie/") != -1 and len(a.split("/")) == 5:
                watchseries(a)
            else:
                print "enter a url of a series or a episode"
        else:
            print "enter a watchseries.to link"
    else:
        print "enter a link "

# watchseries("http://thewatchseries.to/serie/true_blood")
watchseries("http://thewatchseries.to/serie/madame_secretary")
watchseries("http://thewatchseries.to/serie/haven")
watchseries("http://thewatchseries.to/serie/the_librarians_us_")
# watchseries("http://thewatchseries.to/serie/daredevil")
main()
