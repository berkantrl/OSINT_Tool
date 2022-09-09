from Websites import Github,Gitlab,Web_Archive,Medium,Google,SearchCode,Jotform_Forum
from lib.Find import Find 
from lib.Search import Search
import pyfiglet
import threading 
import json 


keywords = Search.get_keywords()


def scan_links():

    print("\n[*]Collecting links.....")
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)
    threads=[]
    # if data['Github'].lower() == 'on':
    #     t1 = threading.Thread(target=Github.get_links(keywords))
    #     t1.start()
    #     threads.append(t1)
    # if data['Gitlab'].lower() == 'on':
    #     t2 = threading.Thread(target=Gitlab.get_links(keywords),daemon=True)
    #     t2.start()
    #     threads.append(t2)
    # if data['Web Archive'].lower() == 'on':
    #     t3 = threading.Thread(target=Web_Archive.get_links(keywords),daemon=True)
    #     t3.start()
    #     threads.append(t3)
    # if data['Google'].lower() == 'on':
    #     t4 = threading.Thread(target=Google.get_links(keywords),daemon=True)
    #     t4.start()
    #     threads.append(t4)
    # if data['Search Code'].lower() == 'on':
    #     t6 = threading.Thread(target=SearchCode.get_links(keywords),daemon=True)
    #     t6.start()
    #     threads.append(t6)
    # if data['Jotform Forum'].lower() == 'on':
    #     t5 = threading.Thread(target=Jotform_Forum.get_links(keywords),daemon=True)
    #     t5.start()
    #     threads.append(t5)
    # if data['Medium'].lower() == 'on':
    #     t7 = threading.Thread(target=Medium.get_links(keywords),daemon=True)
    #     t7.start()
    #     threads.append(t7)


    objects = [Github,Gitlab,Web_Archive,Google,SearchCode,Jotform_Forum,Medium]
    Search_places = ['Github','Gitlab','Web Archive','Google','Search Code','Jotform Forum','Medium']
    for i in data:
        if data[i].lower() == 'on':
            target = objects[Search_places.index(i)] 
            t = threading.Thread(target=target.get_links(keywords))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()
    print("*********************************************")
    print("[*]Collected all links.")
    print("[!]links saved in results.txt.")




def main():
    ascii_banner = pyfiglet.figlet_format("     JOTFORM \nAPI FINDER        ")
    print(ascii_banner)
    scan_links()
    links = Find.get_links()
    print("[*]Finding API in links")
    file = open("apies.txt","a+")
    apies = []
    for link in links:
        control = Find.control_url(link,keywords)
        if control :
            api = Find.find_api(link)
            if api == " ":
                continue
            if api in apies:
                continue
            apies.append(api)
            check_api = Find.control_api(api)
            if check_api:
                file.write(" "+api+"==>"+link+"\n")
    file.close()
    print("[*]Finding iak key...")
    Find.find_apikey_aik()
    print("[!]Checked All links.")
    print("[!]APIes saved in apies.txt")


main()
