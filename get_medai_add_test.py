import requests
from bs4 import BeautifulSoup

url="https://paperswithcode.com"

def get_websit_info(url, process_type="paperwc"): # , tag_name, class_name, process_type
    # Make a request to a web page, and return the status code
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    # Check the status code
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find(class_="col-lg-9 item-content").find('h1')
        # 提取 href 值和标题文本
        web_link = url + a_tags.a['href']
        web_title = a_tags.a.get_text()
    return web_link, web_title

web_link, web_title = get_websit_info(url)
print(web_link,'\n', web_title)


url="https://www.jiqizhixin.com/"

def get_websit_info(url, process_type="paperwc"): # , tag_name, class_name, process_type
    # Make a request to a web page, and return the status code
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    # Check the status code
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')   
        a_tag = soup.find(class_="article-item__right").find("a")
        web_link = url + a_tag.get('href')
        web_title = a_tag.get('alt')
        
    return web_link, web_title
    

web_link, web_title = get_websit_info(url)
print(web_link,'\n', web_title)