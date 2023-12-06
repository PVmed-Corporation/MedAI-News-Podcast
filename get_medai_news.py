import requests
from bs4 import BeautifulSoup
import arxiv
import gnews
# from pytube import Playlist
from youtubesearchpython import Playlist, playlist_from_channel_id

    
# 使用requests和beautifulsoup的函数
def get_websit_info(url, tag_name, class_name, process_type):
    # Make a request to a web page, and return the status code
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

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

        # TODO --连接问题，timeout -- 待用云服务器再尝试
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
        else:
            print("Invalid process type.")
            raise ValueError
        
        return web_link, web_titile   
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        raise ValueError

# 使用内置包的函数
def get_arxiv_summary():
    search = arxiv.Search(
        query="AI, LLM, machine learning, NLP",
        #max_results=st.session_state.arxiv,
        max_results=2,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    ariv_essay = ''
    for result in search.results():
        ariv_essay += result.summary
    return ariv_essay

# TODO --连接问题，timeout
def get_youtube_dojo():
    channel_id = "UCMLtBahI5DMrt0NPvDSoIRQ"
    playlist = Playlist(playlist_from_channel_id(channel_id))
    
    while playlist.hasMoreVideos:
        playlist.getNextVideos()
    machine_title = playlist.videos[0]['title']
    machine_link = playlist.videos[0]['link']
    
    return machine_link, machine_title

# TODO --连接问题，返回是空置
# 这里还有一些可选的变量（如max_result）被设置成常数了
def fetch_gnews_links(query, language='en', country='US', period='1d', start_date=None, end_date=None, max_results=5,
                    exclude_websites=None):
    # Ensure that the exclude_websites parameter is a list
    content = {'title': [], 'summary': [], 'url': []}
    # 初始化 GNews
    google_news = gnews.GNews(language=language, country=country, period=period, start_date=start_date, end_date=end_date,
                        max_results=max_results, exclude_websites=exclude_websites)
    # 根据query获取新闻
    news_items = google_news.get_news(query)
    print(news_items)
    # 提取URLs
    urls = [item['url'] for item in news_items]
    content['title'] = [item['title'] for item in news_items]
    for url in urls:
        content['url'].append(url)
        # content['summary'].append(summarize_website_content(url))
    return content
