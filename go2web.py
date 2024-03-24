import requests
import argparse
import webbrowser
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--url", help="make an HTTP request to the specified URL and print the response")
parser.add_argument("-s", "--search", help="make an HTTP request to search the term using your favorite search engine and print top 10 results")

args = parser.parse_args()


if args.url:
    response = requests.get(args.url, allow_redirects=False)
    if response:
        if response.history:
            print('Request was redirected')
            for resp in response.history:
                print(resp.status_code, resp.url)
            print('Final destination:', response.status_code, response.url)
        else:
            print('Request was not redirected')
        print(f"GET request successful! , Status_code = {response.status_code}")

    if response.status_code == 404:
        print(f"Page not found!, Status code: {response.status_code}")



if args.search:
    headers_Get = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }


    def google(q):
        s = requests.Session()
        q = '+'.join(q.split())
        url = 'https://www.google.com/search?q=' + q + '&oq=+' + q + '+&ie=UTF-8'
        r = s.get(url, headers=headers_Get)
        soup = BeautifulSoup(r.text, "html.parser")
        output = []
        for searchWrapper in soup.find_all('h3'): #this line may change in future based on google's web page structure
            search_tag = searchWrapper.text
            search_link = searchWrapper.findPrevious('a').get('href')
            search_link = search_link.replace("/url?esrc=s&q=&rct=j&sa=U&url=", '')
            if(search_link[0] == 'h'):
                result = {'text': search_tag, 'link': search_link}
                output.append(result)


        return output

    for i in google(args.search):
        print(i)


