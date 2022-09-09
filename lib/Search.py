from random import choice
from re import L
import requests
from bs4 import BeautifulSoup as bs
import httplib2
import mechanicalsoup
import os



class Search:
    

    def extract_links(url:str):
        links = []
        proxies = Search.GetProxy()
        page = requests.get(url,proxies)    
        data = page.text
        soup = bs(data,'lxml')
        for link in soup.find_all('a'):
            if link in links:
                continue
            links.append(link['href'])
        return links



    def extract_links_without_proxies(url:str):
        links = []
        http = httplib2.Http()
        response, content = http.request(url)
        for link in bs(content,'lxml').find_all('a', href=True):
            if link in links:
                continue
            links.append(link['href'])
        return links

    
    def extract_links_with_login_github(url):
        links = []
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
            )
        browser.open("https://github.com")
        browser.follow_link("login")
        browser.select_form('#login form')
        browser["login"] = 'fortest2900' 
        browser["password"] = 'Jotformtest214' 
        resp = browser.submit_selected()

        browser.open(url)
        
        page = browser.page
        for link in page.find_all('a', href=True):
            if link in links:
                continue
            links.append(link['href'])
        return links        


    def GetProxy():
        url = 'https://www.sslproxies.org'
        r = requests.get(url)
        soup = bs(r.content, 'html5lib')
        proxy = choice(list(map(lambda x: x[0]+':'+x[1],list(zip(list(map(lambda x: x.text, soup.find_all('td')[::8])), (map(lambda x: x.text, soup.find_all('td')[1::8])))))))
        return {
            "http": proxy,
            "https": proxy
        }



    def write_file(links):
        file = open("results.txt","a+")
        for link in links:
            file.write(link+ "\n")
        file.close()



    def check_links(link):
        texts = ['search','help','users','settings','features','organizations', 'customer','sponsors','team','enterprise','explore','topics','collections','trending','mobile','signup','login','pricing','marketplace','events','password','site','dashboard','pulls','codespaces','new','issues','notifications','readme','about','api','?q','/m/','signin','gitlab-com','fortest29']
        if link:
            for text in texts:
                if text in link[:14]:
                    return False
        return True



    def clear_links(links,domain):
        results = []
        for link in links:
            is_clear = Search.check_links(link)
            if not is_clear:
                continue
            if link:
                if link[0] == '/':
                    link = f"{domain}{link}"
                else:
                    continue
            else: 
                continue
            if link == domain + "/" :
                continue
            if '#' in link:
                continue
            results.append(link)
        return results


    def clear_links_jotform(links,domain):
        results = [] 
        for link in links:
            if domain in link [:(len(domain)+1)]:
                if link == domain + "/" :
                    continue
                if domain + "/search" in link :
                    continue
                results.append(link)
        return results

    def get_keywords():
        if os.name == "posix":
            file = open("source/keywords.txt","r")
        else: 
            file = open("OSINT_Tool\source\\keywords.txt","r")
        new_keyword = []
        keywords = file.readlines()
        for keyword in keywords:
            new = keyword.replace("\n","")
            new_keyword.append(new)
        return new_keyword 

