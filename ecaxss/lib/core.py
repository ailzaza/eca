from lib.helper.helper import *
from random import randint
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from lib.helper.Log import *
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class core:
    @classmethod
    def load_payloads(cls, filename):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'r') as file:
            return [line.strip() for line in file.readlines()]

    @classmethod
    def generate(cls, eff):
        FUNCTION = cls.load_payloads('payload1.txt')
        payloads = []
        for function in FUNCTION:
            payloads.append("<script>" + function + "</script>")
        return payloads

    @classmethod
    def post_method(cls):
        bsObj = BeautifulSoup(cls.body, "html.parser")
        forms = bsObj.find_all("form", method=True)
        payloads = cls.generate(6)

        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = cls.url

            if form["method"].lower().strip() == "post":
                Log.warning("Target have form with POST method: " + C + urljoin(cls.url, action))
                Log.info("Collecting form input key.....")

                for payload in payloads:
                    keys = {}
                    for key in form.find_all(["input", "textarea"]):
                        try:
                            if key["type"] == "submit":
                                Log.info("Form key name: " + G + key["name"] + N + " value: " + G + "<Submit Confirm>")
                                keys.update({key["name"]: key["name"]})
                            else:
                                Log.info("Form key name: " + G + key["name"] + N + " value: " + G + payload)
                                keys.update({key["name"]: payload})
                        except Exception as e:
                            Log.info("Internal error: " + str(e))

                    Log.info("Sending payload (POST) method...")
                    req = cls.session.post(urljoin(cls.url, action), data=keys)
                    if payload in req.text:
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
        payloads = cls.generate(6)

        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = cls.url

            if form["method"].lower().strip() == "get":
                Log.warning("Target have form with GET method: " + C + urljoin(cls.url, action))
                Log.info("Collecting form input key.....")

                for payload in payloads:
                    keys = {}
                    for key in form.find_all(["input", "textarea"]):
                        try:
                            if key["type"] == "submit":
                                Log.info("Form key name: " + G + key["name"] + N + " value: " + G + "<Submit Confirm>")
                                keys.update({key["name"]: key["name"]})
                            else:
                                Log.info("Form key name: " + G + key["name"] + N + " value: " + G + payload)
                                keys.update({key["name"]: payload})
                        except Exception as e:
                            Log.info("Internal error: " + str(e))

                    Log.info("Sending payload (GET) method...")
                    req = cls.session.get(urljoin(cls.url, action), params=keys)
                    if payload in req.text:
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
        payloads = cls.generate(6)

        for a in links:
            url = a["href"]
            if not (url.startswith("http://") or url.startswith("https://") or url.startswith("mailto:")):
                base = urljoin(cls.url, a["href"])
                query = urlparse(base).query
                if query != "":
                    Log.warning("Found link with query: " + G + query + N + " Maybe a vuln XSS point")

                    for payload in payloads:
                        query_payload = query.replace(query[query.find("=")+1:len(query)], payload, 1)
                        test = base.replace(query, query_payload, 1)

                        query_all = base.replace(query, urlencode({x: payload for x in parse_qs(query)}))

                        Log.info("Query (GET) : " + test)
                        Log.info("Query (GET) : " + query_all)

                        if not url.startswith("mailto:") and not url.startswith("tel:"):
                            _respon = cls.session.get(test, verify=False)
                            if payload in _respon.text or payload in cls.session.get(query_all).text:
                                Log.high("Detected XSS (GET) at " + _respon.url)
                                with open("xss.txt", "a") as file:
                                    file.write(str(_respon.url) + "\n\n")
                            else:
                                Log.info("Parameter page using (GET) payloads but not 100% yet...")
                        else:
                            Log.info("URL is not an HTTP url, ignoring")

    @classmethod
    def main(cls, url, payload, method=2, user_agent=None):
        print(W + "*"*15)
        cls.payload = payload
        cls.url = url

        cls.session = requests.Session()
        
        # Set User-Agent jika ada
        if user_agent:
            cls.session.headers.update({'User-Agent': user_agent})

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
            Log.info("Connection established " + G + str(ctr.status_code))

        if method >= 2:
            cls.post_method()
            cls.get_method()
            cls.get_method_form()
        elif method == 1:
            cls.post_method()
        elif method == 0:
            cls.get_method()
            cls.get_method_form()
