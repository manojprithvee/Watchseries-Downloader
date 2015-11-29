# TODO add a expire date to the data.json 
import requests, re, os, base64, subprocess, time, sys, notify2, json, atexit
import lxml.html as lh

FAIL = '\033[91m'
ENDC = '\033[0m'
notify2.init('watchseries downloader')
pkl_file = open('test.json', 'rb')
data = json.load(pkl_file)
gorillavialist = list()


def onexit():
    print "saving status.."
    output = open('test.json', 'wb')
    json.dump(data, output)
    os.system("setterm -cursor on")
    os.system("stty echo")
    output.close()
    if "-p" in sys.argv:
        os.system("poweroff")


atexit.register(onexit)


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


def gorillavia(link, name, season, episold, s_name):
    print "S_" + str(season) + "E_" + str(episold)
    try:
        if link.find("gorillavid.in") == -1:
            print FAIL + "This has no gorillavid Links" + ENDC
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
            if out.find("416 Requested Range Not Satisfiable") == -1:
                n = notify2.Notification("File Downloaded:", namel.split("/")[-1],
                                         "notification-network-ethernet-connected")
                n.show()
            print "\n------------------------------------------------------\n"
    except Exception, e:
        print FAIL + str(e) + ENDC
        wait_for_internet()
        # gorillavia(link,name,season,episold,s_name)
        return


def leve1(link, i, j, s_name):
    try:
        a = requests.get(link,timeout=1)
        time.sleep(1)
    except Exception, e:
        print FAIL + str(e) + ENDC
        wait_for_internet()
        # leve1(link,i,j,s_name)
        return
    doc = lh.fromstring(a.text)
    final = doc.xpath('//*[2]/td[2]/a/@href')
    # print link
    name = doc.xpath("//title/text()")[0]
    name = name.split(" - ")[1]
    if final!=[]:
    	gorillavialist.append([base64.b64decode(final[0].replace("/cale.html?r=", "")[:56]), name, i, j, s_name])
    else:
    	print "no links found"


def rundownload(s_name):
    global data
    data[s_name]["episold_list"] = list(gorillavialist)
    season = -1
    episold = -1
    if "last_downloaded" in data[s_name]:
        season, episold = data[s_name]['last_downloaded']
    for i in gorillavialist:
        if i[2] >= season and i[3] > episold:
            gorillavia(i[0], i[1], i[2], i[3], i[4])
            season = -1
            episold = -1


def watchseries(link):
    s_name = link.split("/")[-1]
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
                        print ("s" + str(i) + "_e" + str(j))
                        leve1("http://thewatchseries.to" + x, i, j, s_name)
        data[s_name] = {}
        data[s_name]["lastupdate"]=int(round(time.time() * 1000))
        rundownload(s_name)
    else:
        print "previous data found and starting resuming"
        global gorillavialist
        gorillavialist = data[s_name]["episold_list"]
        rundownload(s_name)


def main():
    pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    a = raw_input("enter the watchseries.to Link:")
    if pattern.match(a):
        if a.find("watchseries.to") != -1:
            if a.find("/episode/") != -1 and len(a.split("/")) == 5:
                b = raw_input("enter the season number:")
                c = raw_input("enter the episode number:")
                d = raw_input("enter the episode name:")
                leve1(a, b, c, d)
            elif a.find("/serie/") != -1 and len(a.split("/")) == 5:
                watchseries(a)
            else:
                print "enter a url of a series or a episode"
        else:
            print "enter a watchseries.to link"
    else:
        print "enter a link "


# watchseries("http://thewatchseries.to/serie/avengers_assemble")
# watchseries("http://thewatchseries.to/serie/The_Blacklist")
# watchseries("http://thewatchseries.to/serie/madame_secretary")
watchseries("http://thewatchseries.to/serie/daredevil")
# watchseries("http://thewatchseries.to/serie/the_librarians_us_")
# watchseries("http://thewatchseries.to/serie/daredevil")
# main()
