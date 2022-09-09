from lib.Search import Search
import googlesearch
import gitlab 
# from github import Github as Gh 

all_links = []
count = 0

class Github:
    

    def get_links(keywords):

        global all_links 
        global count
        domain = "https://github.com"
        for keyword in keywords:
            for page in range(1,10):
                url = f"https://github.com/search?p={page}&q={keyword}&type=Code"
                links = Search.extract_links_with_login_github(url)
                results = Search.clear_links(links,domain)
                for link in results:
                    if link in all_links:
                        results.remove(link)
                for link in results:
                    all_links.append(link)
                count = count + len(results)
                Search.write_file(results)
                if len(results) == 0:
                    break

        # token = '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'
        
        # for keyword in keywords:
        #     g = Gh(token)
        #     results = [] 
        #     query = keyword
        #     result = g.search_code(query)    
        #     for repo in result:
        #         results.append(repo.html_url)
        #     Search.write_file(results)        
        #     time.sleep(50)


class Web_Archive:


    def get_links(keywords):

        global all_links 
        global count
        domain = "https://archive.org"
        for keyword in keywords:
            for page in range(1,10):
                url = f"https://archive.org/search.php?query=%28{keyword}%29&page={page}"
                links = Search.extract_links_without_proxies(url)
                results = Search.clear_links(links,domain)
                for link in results:
                    if link in all_links:
                        results.remove(link)
                for link in results:
                    all_links.append(link)
                count = count + len(results)
                Search.write_file(results)
                if len(results) == 0:
                    break



class Google:

    def get_links(keywords):

        global count
        results = []
        for keyword in keywords:
            query = f'"{keyword}"'
            for j in googlesearch.search(query, tld="co.in",  stop=10, pause=2):
                results.append(j)
            count = count + len(results)
        Search.write_file(results)



class SearchCode:


    def get_links(keywords):

        global all_links 
        global count
        domain = "https://searchcode.com"
        for keyword in keywords:
            for page in range(10):
                url = f"https://searchcode.com/?q={keyword}&p={page}"
                links = Search.extract_links(url)
                results = Search.clear_links(links,domain)
                for link in results:
                    if link in all_links:
                        results.remove(link)
                for link in results:
                    all_links.append(link)
                if len(results) == 0:
                    break
                count = count + len(results)
                Search.write_file(results)

class Jotform_Forum:


    def get_links(keywords):

        global all_links 
        global count
        domain = "https://www.jotform.com/answers"
        for keyword in keywords:
            for page in range (0,200,10):
                url = f"https://www.jotform.com/answers/search.php?search={keyword}&from={page}"
                links = Search.extract_links_without_proxies(url)
                results = Search.clear_links_jotform(links,domain)
                for link in results:
                    if link in all_links:
                        results.remove(link)
                for link in results:
                    all_links.append(link)
                if len(results) == 0:
                    break
                count = count + len(results)
                Search.write_file(results)


class Medium:


     def get_links(keywords):

        global count
        results = []
        for keyword in keywords:
            query = f'"{keyword}" site:medium.com'
            for j in googlesearch.search(query, tld="co.in",  stop=10, pause=2):
                results.append(j)
            count = count + len(results)
        Search.write_file(results)


class Gitlab:


    def get_links(keywords):
 
        results = [] 
        titles = ['blobs','projects']
        gl = gitlab.Gitlab(private_token='glpat-6xvcJVsfs1jCHDfKyGp8')
        for key in keywords:
            for title in titles: 
                for a in gl.search(title,key):
                    url = 'https://gitlab.com/gitlab-com/'+a['path']
        Search.write_file(results)

keywords = ["JotformAPIClient"]
a = Github.get_links(keywords)