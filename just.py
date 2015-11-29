import urllib2
import libxml2
import os
import thread
import time
def level2link(head,a,url):
	url=url.replace('"',"")
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib2.Request(url,headers=hdr)
	f = urllib2.urlopen(req)
	html = f.read()
	f.close()
	parse_options = libxml2.HTML_PARSE_RECOVER + \
	libxml2.HTML_PARSE_NOERROR + \
	libxml2.HTML_PARSE_NOWARNING
	doc = libxml2.htmlReadDoc(html,'',None,parse_options)
	epview=doc.xpathEval('//iframe/@src')
	try:
		x=str(epview[2]).replace("src=","").replace('"',"")+"\n"+str(epview[3]).replace("src=","").replace('"',"")+"\n"+str(epview[4]).replace("src=","").replace('"',"")+"\n"
		head=head.replace("/","").replace("<","").replace(">","").replace(":","").replace("|","").replace("?","").replace("*","").replace("...","")
		a=a.replace("/","").replace("<","").replace(">","").replace(":","").replace("|","").replace("?","").replace("*","").replace("\xe2\x80\xa6","...").replace("...","")
	except:
		x=str(epview[2]).replace("src=","").replace('"',"")
		head=head.replace("/","").replace("<","").replace(">","").replace(":","").replace("|","").replace("?","").replace("*","").replace("...","")
		a=a.replace("/","").replace("<","").replace(">","").replace(":","").replace("|","").replace("?","").replace("*","").replace("\xe2\x80\xa6","...").replace("...","")
	try:
		os.makedirs("just/"+head)
	except Exception, e:
		pass

	f=open("just/"+head+"/"+a,"w")
	f.write(x)



def level1link(head,url):
	#url='file:///C:/Users/manoj prithvee/Videos/www/epi.html'
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib2.Request(url,headers=hdr)
	f = urllib2.urlopen(req)
	html = f.read()
	f.close()
	parse_options = libxml2.HTML_PARSE_RECOVER + \
	libxml2.HTML_PARSE_NOERROR + \
	libxml2.HTML_PARSE_NOWARNING
	doc = libxml2.htmlReadDoc(html,'',None,parse_options)
	listep=doc.xpathEval('//ul[@id="archive-results"]/li/a/text()')
	eplink=doc.xpathEval('//ul[@id="archive-results"]/li/a/@href')
	x=""
	i=0
	for iq in listep:
		try:
			thread.start_new_thread(level2link,(head,str(iq),str(eplink[i]).strip().replace("\n","").replace("href=","")))
			i=i+1
			if(i%20==0):
				time.sleep(5)
		except:
			pass
	print head
url='http://www.justanimedubbed.tv/full-list/'
hdr = {'User-Agent':'Mozilla/5.0'}
req = urllib2.Request(url,headers=hdr)
f = urllib2.urlopen(req)
html = f.read()
f.close()
parse_options = libxml2.HTML_PARSE_RECOVER + \
libxml2.HTML_PARSE_NOERROR + \
libxml2.HTML_PARSE_NOWARNING
doc = libxml2.htmlReadDoc(html,'',None,parse_options)	
div = doc.xpathEval('//div[@class="ddmcc"]/ul/ul/li/a/text()')
q= doc.xpathEval('//div[@class="ddmcc"]/ul/ul/li/a/@href')
for ij in div[1500:]:
	try:
		thread.start_new_thread(level1link,(str(ij),str(q[div.index(ij)]).replace("href=","").replace('"','')))
	except:
		pass
while 1:
   pass