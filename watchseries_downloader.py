# TODO add pause button
'''
options 
-reverse to start from latest episold
-p to poweroff after download is Completed
-l <number> limit the download in kb
'''
import requests, re, os, base64, subprocess, time, sys, json, atexit,threading,getpass
import lxml.html as lh,platform
Ostype=platform.system()
FAIL = '\033[91m'
ENDC = '\033[0m'
data={}
gorillavialist = list()
notification_complete=""
filread=open("test.json","r")
s_names=json.loads(filread.read())
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
    print 'Waiting for internet..',
    while True:
        p = subprocess.Popen("ping -c 1 8.8.8.8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        output = p.stdout.read()
        if output.find("100% packet loss") == -1 and output.find("connect: Network is unreachable") == -1:
            return
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            
        

def Run_process(exe,namel,season, episold,s_name):
    if Ostype=="Windows":
        p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if Ostype=="Linux":
        p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, executable="/bin/bash")
    final = ""
    abc=0
    while True:
        retcode = p.poll()  # returns None while subprocess is running
        out = p.stdout.readline()
        out = out.replace(".......... ", "").replace(",......... ", "").replace(",,........ ", "").replace(
            ",,,....... ", "").replace(",,,,...... ", "").replace(",,,,,..... ", "").replace(",,,,,,.... ", "").replace(
            ",,,,,,,... ", "").replace(",,,,,,,,.. ", "").replace(",,,,,,,,,. ", "").replace(",,,,,,,,,, ", "").replace("..", "")
        temp = out
        global data
        if len(temp) > 30:
            pass
            # print temp,
        if len(temp) < 30:
            if temp.find("skipping") == -1:
                a = out.strip().split(" ")
                if a != [""]:
                    a = [x for x in a if x != ""]
                    print("\033[K\033[07m" + "Downloaded: " + a[0] + "B Completed: " + a[1] + " Speed: " + a[
                        2] + "B\s Time : " + a[3] +" episold: " + "S_" + str(season) + "E_" + str(episold) + "\033[0m \r"),

        final = final + out
        if abc==0 and final.find("100%")!=-1:
            abc=1
            global notification_complete
            print "S_" + str(season) + "E_" + str(episold)+"\n-------------------------------Completed----------------------------------"
            notification_complete=notification_complete+s_name +'Season '+str(season)+" Episold "+str(episold)+"\n"
        if abc==0 and final.find("416 Requested Range Not Satisfiable")!=-1:
            abc=1
            print "S_" + str(season) + "E_" + str(episold)+"\n---------- Its Already Downloaded ----------"

        if retcode is not None:
            os.system("setterm -cursor on && stty echo")
            return final
        


def gorillavia(link, name, season, episold, s_name,try1):

    # try:
        print link
        if link.find("gorillavid.in") == -1:
            print FAIL + "S_" + str(season) + "E_" + str(episold) +"\nThis has no gorillavid Links" + ENDC
        elif(try1==4):
            print FAIL + "S_" + str(season) + "E_" + str(episold) +"\nTryed 3 Time And Failed" + ENDC
            return
        else:
            a = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Moto G Build/LMY48Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36","Upgrade-Insecure-Requests": 1})
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', a.text)
            for i in urls:
                if i.find(".mp4") != -1:
                    urls = i
                    break
            if Ostype=="Windows":
                try:
                    os.makedirs("C:\Users\\"+getpass.getuser()+"\Downloads\watchseries\\" + s_name + "\Season-" + str(season)) 
                except:
                    pass
                namel = "C:\Users\\"+getpass.getuser()+"\Downloads\watchseries\\" + s_name + "\\Season-" + str(
                season) + "\\" + s_name + "_S" + str(season) + "E" + str(episold) + "-" + name + ".mp4"
            elif Ostype=="Linux":
                try:
                    os.makedirs("/home/"+getpass.getuser()+"/Downloads/watchseries/" + s_name + "/Season-" + str(season)) 
                except:
                    pass
                namel = "/home/"+getpass.getuser()+"/Downloads/watchseries/" + s_name + "/Season-" + str(
                season) + "/" + s_name + "_S" + str(season) + "E" + str(episold) + "-" + name + ".mp4"
            if "-l" in sys.argv:
                try:
                    print "speed"
                    speed=int(sys.argv[sys.argv.index("-l")+1])
                    out = Run_process('wget.exe  -c --limit-rate='+str(speed)+'k -O "' + namel + '" ' + urls,namel,season, episold,s_name)
                    if out.find("100%")!=-1:
						for j in s_names:
							if j[0]==s_name:
								j[1]=season
								j[2]=episold+1
						filwite=open("test.json","w")
						filwite.write(json.dumps(s_names))
						filwite.close()
                except Exception, e:
                    print FAIL + "S_" + str(season) + "E_" + str(episold)+"\n" +str(e) + ENDC
                    print "enter a number for speed"
                    os._exit(0)
            else:
                out = Run_process('wget.exe  -c -O "' + namel + '" ' + urls,namel,season, episold,s_name)
                if out.find("100%")!=-1:
						for j in s_names:
							if j[0]==s_name:
								j[1]=season
								j[2]=episold+1
						filwite=open("test.json","w")
						filwite.write(json.dumps(s_names))
						filwite.close()
                if out.find("failed:")!=-1:
                    gorillavia(link, name, season, episold, s_name,try1+1)
                    
    # except Exception, e:
    #     print FAIL + "S_" + str(season) + "E_" + str(episold) +"\n"+str(e) + ENDC
    #     global client
    #     wait_for_internet()
    #     if try1==1 and str(e).find("HTTPConnectionPool")==-1:
    #         notify("WS Downloader S_" + str(season) + "E_" + str(episold),str(e),1,1)
    #     gorillavia(link,name,season,episold,s_name,try1+1)
        


def leve1(link, i, j, s_name,try1):
    print "\nS_"+str(i)+"E_"+str(j),
    if(try1==4):
        print FAIL + "tryed 3 time and failed" + ENDC
        return
    try:
        a = requests.get(link,timeout=10)
    except Exception, e:
        print FAIL + "S_"+str(i)+"E_"+str(j)+"\n "+str(e) + ENDC
        wait_for_internet()
        leve1(link,i,j,s_name,try1+1)
        return
    doc = lh.fromstring(a.text)
    final = doc.xpath('//a[@class="buttonlink"]/@href')
    # print link
    name = doc.xpath("//title/text()")[0]
    name = name.split(" - ")[1]
    if final!=[]:
        gorillavialist.append([base64.b64decode(final[1].replace("/cale.html?r=", "")[:56]), name, i, j, s_name])
    else:
        print "no links found"


def leve1_epi(link,i,j,s_name,try1):
    if(try1==4):
        print FAIL + "tryed 3 time and failed" + ENDC
        return
    try:
        a=requests.get(link)
    except Exception, e:
        print FAIL + "S_" + str(season) + "E_" + str(episold) +"\n"+str(e)+ ENDC
        wait_for_internet()
        leve1_epi(link,i,j,s_name,try1+1)
        return
    html=a.text.encode('ascii', 'ignore').decode('ascii')
    doc = lh.fromstring(a.text)
    final = doc.xpath('//a[@class="buttonlink"]/@href')
    name=doc.xpath("//title/text()")[0]
    name=name.split(" - ")[1]
    gorillavia(base64.b64decode(final[1].replace("/cale.html?r=","")[:56]),name,i,j,s_name,1)

def rundownload(s_name):
    print "enter rundownload"
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
                    
                    # threads.append(threading.Thread(target=gorillavia,args=(i[0], i[1], i[2], i[3], i[4],1)))
                    gorillavia(i[0], i[1], i[2], i[3], i[4],1)
    # index=1
    # sublist=list()
    # for a in threads:
    #     if index%2==0:
    #         for i in sublist:
    #             i.join()
    #         sublist=list()
    #     a.start()
    #     sublist.append(a)
    #     index=index+1
    # for i in sublist:
    #     i.join()
    gorillavialist=list()


def watchseries(link,start_season=0,start_episold=0,final_season=50000,final_episold=50000):
    wait_for_internet()
    s_name = link.split("/")[-1]
    print "\n"+s_name.replace("_"," ")
    datamining(link,s_name,start_season,start_episold,final_season,final_episold)
    rundownload(s_name)
    gorillavialist=list()

def datamining(link,s_name,start_season,start_episold,final_season,final_episold,try1=1):
    if(try1==4):
        print FAIL + "tryed 3 time and failed" + ENDC
        return
    try:
        a = requests.get(link)
    except Exception, e:
        print FAIL + str(e) + ENDC
        wait_for_internet()
        datamining(link,s_name,start_season,start_episold,final_season,final_episold,try1+1)
        return
    doc = lh.fromstring(a.text)
    epview = doc.xpath('//meta[@itemprop="url"]/@content')
    threads=list()
    for i in range(50):
        for j in range(200):
            for x in epview:
                if x.find("s" + str(i) + "_e" + str(j) + ".html") != -1:
                    if i >= start_season:
                        if j >= start_episold-1:  
                            if i<=final_season: 
                                if j<=final_episold:
                                    # leve1("http://thewatchseries.to" + x, i, j, s_name,1)
                                    threads.append(threading.Thread(target=leve1,args=("http://thewatchseries.to" + x, i, j, s_name,1)))
        start_episold=0
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
                leve1_epi(a, b, c, d)
            elif a.find("/serie/") != -1 and len(a.split("/")) == 5:
                
                if raw_input("do u want to start form the top (y or n)").lower()=="y":
                    watchseries(a)
                else:
                    watchseries(a,int(raw_input("enter the sesaon number")),int(raw_input("enter the Episold number")))
            else:
                print "enter a url of a series or a episode"
        else:
            print "enter a watchseries.to link"
    else:
        print "enter a link "
if "--main" in sys.argv:
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
            # raise ValueError("watchseries-Need Exactly 3 Arguments")