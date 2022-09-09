import requests
from bs4 import BeautifulSoup as bs
import urllib.request as urllib2
import os 
import re 
import time 


class Find:
    
    def control_url(url,keywords):
        """This Function checks url and searches for keyword on website. Returns True if the url has a keyword. it also checks the status code."""
        
        r = requests.get(url)
        if r.status_code != 200 and r.status_code != 302:
            return False
        try:
            soup = bs(r.content,"html.parser")
        except:
            time.sleep(5)
            soup = bs(r.content,"lxml")
        for keyword in keywords:
            if keyword in soup.get_text():
                return True
            else:
                return False
            
    def extract_api_lines(url,keys):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

        req = urllib2.Request(url, headers=hdr)

        lines = urllib2.urlopen(req).readlines()

        api_lines = []
        for line in lines:
            line = ''.join(map(chr, line))
            line = line.lstrip()
            line = line.replace("\n","")
            for key in keys:
                if (key) in str(line): 
                    api_lines.append(str(line))  
        return api_lines


    def find_api(url):
        keys = Find.get_keys()
        api_lines = Find.extract_api_lines(url,keys)
        for line in api_lines:
            clear_text = Find.cleanhtml(line)
            api = Find.extract_api(clear_text)
            try:
                if api == "YOUR API KEY" or api == "'YOUR API KEY'" or api == "YOUR API CODE":
                    return " "
                if api[0] == '"' or len(api)== 32 :
                    return api 
                else: 
                    api_lines= Find.extract_api_lines(url,[api])
                    for line in api_lines:
                        clear_text2 = Find.cleanhtml(line)
                        clear_text2 = clear_text2.lstrip()
                        api = Find.extract_api_in_value(clear_text2)
                        if api != " ":
                            return api 
            except :
                continue
        return " " 


    def extract_api(line):
        line = line.lstrip()
        symbols = ["(",",",")",":"] 
        start = 0
        end  = 0  
        count = 0 
        for symbol in symbols: 
            position = line.find(symbol,end)
            if position == (-1) : 
                continue 
            else: 
                start = end
                end = position
                count +=1
                if count == 2:
                    break
        
        if count == 1:
            api = line[(end+1):]
        else: 
            api = line[(start+1):end]
        clear_api = api.replace(";","") 
        clear_api = clear_api.lstrip()
        return clear_api



    def extract_api_in_value(line):
        
        symbols = ["="] 
        start = 0
        for symbol in symbols: 
            position = line.find(symbol)
            if position == (-1) : 
                return " "
            else: 
                start = position
                
        return (line[(start+1):])

    def get_keys():
        if os.name == "posix":
            file = open("source/keys.txt","r")
        else: 
            file = open("OSINT_Tool\source\\keys.txt","r")
        new_keys = []
        keys = file.readlines()
        for key in keys:
            new_key = key.replace("\n","")
            new_keys.append(new_key)
        return new_keys

    def cleanhtml(raw_html):
        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(CLEANR, '', raw_html)
        return cleantext

    
    def control_api(api):
        api = api.lstrip()
        url = f"https://api.jotform.com/user?apiKey={api}"
        r = requests.get(url)
        try : 
            status_code = r.status_code
            if status_code == 200 or status_code == 302:
                return True 
            return False 
        except : 
            return False 
    
    def get_links():
        new_keywords = []
        if os.name == "posix":
            file = open("results.txt","r")
        else: 
            file = open("results.txt","r")

        keywords = file.readlines()
        for keyword in keywords:
            new = keyword.replace("\n","")
            new_keywords.append(new)
        return new_keywords       

    def find_apikey_aik():
        keys = ["apiKey","iak"] 
        urls = ["api.jotform.com","jotform.com","*.eu-api.jotform.com"]
        file = open("apies.txt","a+")
        apies = [] 
        for url in urls:
            links = [f"https://web.archive.org/cdx/search/cdx?url={url}/*&collapse=urlkey&output=text&fl=original",f"http://wwwb-dedup.us.archive.org:8083/cdx/search?url={url}/*&matchType=domain&collapse=digest&output=text&fl=original,timestamp"]
            for link in links: 
                lines = Find.extract_api_lines(link,keys)
                for line in lines : 
                    if "apiKey" in line:
                        key = "apikey"
                    else : 
                        key = "iak"
                    clear_text = Find.cleanhtml(line)
                    api = Find.extract_api_in_value(clear_text)
                    if key == "apikey":
                        api = api[:32]
                    elif key == "iak":
                        api = api[:49]
                    else: 
                        continue
                    if api in apies:
                        continue
                    apies.append(api)

                    check = Find.control_api(api)
                    if check:
                        file.write(" "+api+"==>"+link+" "+clear_text+"\n")
        file.close()

