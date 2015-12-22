import execjs,requests,lxml.html as lh,re,os,time
def main(link="",times=0.1):
	try:
		ctx = execjs.compile("""var END_OF_INPUT=-1;var arrChrs=new Array("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","+","/");var reversegetFChars=new Array;for(var i=0;i<arrChrs.length;i++){reversegetFChars[arrChrs[i]]=i}var getFStr;var getFCount;function ntos(e){e=e.toString(16);if(e.length==1)e="0"+e;e="%"+e;return unescape(e)}function readReversegetF(){if(!getFStr)return END_OF_INPUT;while(true){if(getFCount>=getFStr.length)return END_OF_INPUT;var e=getFStr.charAt(getFCount);getFCount++;if(reversegetFChars[e]){return reversegetFChars[e]}if(e=="A")return 0}return END_OF_INPUT}function readgetF(){if(!getFStr)return END_OF_INPUT;if(getFCount>=getFStr.length)return END_OF_INPUT;var e=getFStr.charCodeAt(getFCount)&255;getFCount++;return e}function setgetFStr(e){getFStr=e;getFCount=0}function getF(e){setgetFStr(e);var t="";var n=new Array(4);var r=false;while(!r&&(n[0]=readReversegetF())!=END_OF_INPUT&&(n[1]=readReversegetF())!=END_OF_INPUT){n[2]=readReversegetF();n[3]=readReversegetF();t+=ntos(n[0]<<2&255|n[1]>>4);if(n[2]!=END_OF_INPUT){t+=ntos(n[1]<<4&255|n[2]>>2);if(n[3]!=END_OF_INPUT){t+=ntos(n[2]<<6&255|n[3])}else{r=true}}else{r=true}}return t}function doit(e){return unescape(getF(getF(e)))}""")
		if link=="":
			link=raw_input("Enter the link: ")
		a=requests.get(link)
		doc=lh.fromstring(a.text)
		x=doc.xpath("//script/text()")[2]
		name=doc.xpath("//h1/strong/font/text()")[0]
		name=name.replace("Watch ","").replace(" Online","")
		print name
		x=re.findall("(?<=')[^']+(?=')",x)[0]
		x=ctx.call("doit",x)
		x=re.findall('(?<=src=")[^"]+(?=")',x)[0]
		a=requests.get(x, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Moto G Build/LMY48Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36","Upgrade-Insecure-Requests": 1})
		print a.text
		print x
		x=re.findall('(?<=360p"},{file:")[^#]+(?=",label:"720p")',a.text)[0]
		os.system("mkdir -p /home/manoj/Downloads/putlocker/")
		namel = "'/home/manoj/Downloads/putlocker/"+name+".mp4'"
		os.system('export http_proxy=http://127.0.0.1:8118 & wget -c -O'+ namel+' '+x)
	except:
		time.sleep(times)
		main(link,times+0.1)
		return
main()