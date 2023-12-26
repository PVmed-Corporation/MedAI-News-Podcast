import requests
from bs4 import BeautifulSoup
import arxiv
from gnews import GNews
# from pytube import Playlist
from youtubesearchpython import Playlist, playlist_from_channel_id

    
# 使用requests和beautifulsoup的函数
def get_websit_info(url, tag_name, class_name, process_type):
    # Make a request to a web page, and return the status code
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    
    # Check the status code
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 爬取OPENAI_link
        if process_type == "openai": 
            # 查找具有特定类名的<a>标签
            target_link = soup.find(tag_name, class_=class_name)
            if target_link:
                # 将基本 URL 与相对路径结合
                web_link = url + target_link['href']
                response = requests.get(web_link, headers=headers)
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.content, 'html.parser')
                h1_tag = soup.find("h1", class_="f-display-2")
                if h1_tag:
                    web_titile = h1_tag.text.strip()
                else:
                    print("Couldn't find the <h1> tag with the specified class on the page.")
                    raise ValueError
            else:
                print("Couldn't find the target post URL.")
                raise ValueError  
               
        # 爬取lexfridman_link
        elif process_type == "lexfridman": 
            transcript_link_element = soup.find(tag_name, string="Transcript")
            if transcript_link_element:
                web_link = transcript_link_element['href']
                response = requests.get(web_link, headers=headers)
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.content, 'html.parser')
                h1_tag = soup.find("h1", class_="entry-title")
                if h1_tag:
                    web_titile = h1_tag.text.strip()
                else:
                    print("Couldn't find the <h1> tag with the specified class on the page.")
                    raise ValueError
            else:
                print("Couldn't find the target post URL.")
                raise ValueError   

        # 爬取苹果博客link & title
        elif process_type == "apple": 
            article = soup.select_one(tag_name)
            if article:
                web_link = url + article['href']
                # 根据提供的HTML片段，定位到文章的标题和链接
                web_titile = article.text
            else:
                print("Couldn't find the target post URL.")
                raise ValueError

        # 爬取nvida link & title
        elif process_type == "nvidia":  
            ul_elems = soup.find_all(tag_name)
            all_links = []
            # 从所有 <ul> 元素中提取链接和文本
            for ul_elem in ul_elems:
                links = [(link.get('href'), link.text) for link in ul_elem.find_all('a')]
                all_links.extend(links)
            # 提取指定链接文本对后的第一个链接和文本
            found = False
            for link, text in all_links:
                # print("text1 is", text)
                if found:
                    web_link = link
                    web_titile = text
                    break
                if link == url and text == class_name:
                    found = True
            if not found:
                print("Couldn't find the target post URL.")
                raise ValueError
            
        # 爬取aws link & title
        elif process_type == "aws":  
            articles = soup.find_all(tag_name, class_=class_name)
            if articles:
                web_link = articles[0].find('a')['href']
                web_titile = articles[0].find('h2').text
            else:
                print("Couldn't find the target post URL.")
                raise ValueError
        
        # 爬取microsoft link & title
        elif process_type == "microsoft":  
            # 由于网站可能有多个这样的链接，我们只选择第一个匹配的项
            link_element = soup.find(tag_name, class_=class_name)
            if link_element:
                web_link = link_element['href']
                web_titile = link_element.h3.text.strip()
            else:
                print("Couldn't find the target post URL.")
                raise ValueError

        # 爬取techcrunch link & title
        elif process_type == "techcrunch":  
            # 由于网站可能有多个这样的链接，我们只选择第一个匹配的项
            articles = soup.select('.post-block__title a')
            if articles:
                web_link = articles[0]['href']
                web_titile = articles[0].text
            else:
                print("Couldn't find the target post URL.")
                raise ValueError

        # 爬取机器之心信息
        elif process_type == "机器之心":  
            articles = soup.find(class_=class_name).find("a")
            web_time = soup.find('time', class_='js-time-ago').get_text(strip=True)
            if articles:                
                web_titile = articles.get('alt')
                web_link = url + articles.get('href')
            else:
                print("Couldn't find the target post URL.")
                raise ValueError  
                    
        # 爬取paper with code信息
        elif process_type == "paperwithcode":  
            articles = soup.find(class_=class_name).find('h1')
            web_time = soup.find(class_=class_name).find('span', class_='author-name-text item-date-pub').get_text()
            print("articles:", articles)
            if articles:
                # 提取 href 值和标题文本
                web_link = url + articles.a['href']
                web_titile = articles.a.get_text()
            else:
                print("Couldn't find the target post URL.")
                raise ValueError        
         
        # auntminnie
        elif process_type == "auntminnie":
            soup = BeautifulSoup(response.content, 'html.parser')   
            a_tag = soup.find(class_=class_name).find(tag_name)
            web_link = url + a_tag.get('href')
            web_titile  = a_tag.get_text()
            # 获取时间
            response = requests.get(web_link, headers=headers)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.content, 'html.parser')
            web_time = soup.find(class_="author-published-node__content-published").get_text()

        # auntminnie
        elif process_type == "mobihealthnews":
            soup = BeautifulSoup(response.content, 'html.parser')   
            a_tag = soup.find(class_=class_name).find(tag_name)
            web_link = url + a_tag.get('href')
            web_titile = a_tag.get_text()
            web_time = soup.find('ul', class_='sponsored-author-create top-story').find('li', class_="last").get_text(strip=True)

        # natureBME
        elif process_type == "natureBME" :
            soup = BeautifulSoup(response.content, 'html.parser')   
            a_tag = soup.find(class_=class_name).find(tag_name)
            web_link = a_tag.get('href')
            web_titile = a_tag.get_text()

        return web_link, web_titile, web_time   
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        raise ValueError
        
# 使用内置包的函数
def get_arxiv_summary(_arxiv, query, max_results):
    search = arxiv.Search(
        query=query,
        # primary_category=
        # max_results=st.session_state.arxiv,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    for result in search.results():
        _arxiv.get_page(result.entry_id, result.title)
        # _arxiv.get_content(result.summary)

    return

def get_youtube_dojo(_youtb, channel_id):
    # use Playlist get info
    playlist = Playlist(playlist_from_channel_id(channel_id))
    
    while playlist.hasMoreVideos:
        playlist.getNextVideos()
    machine_title = playlist.videos[0]['title']
    machine_link = playlist.videos[0]['link']
    
    _youtb.get_page(machine_link, machine_title)

    return

def fetch_gnews_links(_google, query, max_results=3):
    # 初始化 GNews
    google_news = GNews(language='en', country='cn', period='1d',
                        start_date=None, end_date=None,
                        max_results=max_results, exclude_websites=None)

    # 根据query获取新闻
    news_items = google_news.get_news(query)
    for gn in news_items:
        _google.get_page(gn.get('url'), gn.get('title'))
        
    return

