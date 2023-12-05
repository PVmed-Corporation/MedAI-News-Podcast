import requests
from bs4 import BeautifulSoup
import arxiv

# 使用requests和beautifulsoup的函数
def get_info(url, tag_name, class_name, process_type):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200: # 检测网站状态
        soup = BeautifulSoup(response.content, 'html.parser')

        if process_type == 1: #爬取OPENAI_link
            # 查找具有特定类名的<a>标签
            target_link = soup.find(tag_name, class_=class_name)
            if target_link:
                # Combining base URL with the relative path
                post_url = url + target_link['href']
                return post_url
            else:
                print("Couldn't find the target post URL.")
                return None

        if process_type == 2: # 爬取title
            h1_tag = soup.find(tag_name, class_=class_name)
            if h1_tag:
                return h1_tag.text.strip()
            else:
                print("Couldn't find the <h1> tag with the specified class on the page.")
                return None

        if process_type == 3: # 爬取lexfridman_link
            transcript_link_element = soup.find('a', string="Transcript")
            if transcript_link_element:
                return transcript_link_element['href']
            else:
                return None

        if process_type == 4: # 爬取苹果博客link&title
            article = soup.select_one('h3.post-title a')
            apple_link = 'https://machinelearning.apple.com' + article['href']
            # 根据提供的HTML片段，定位到文章的标题和链接
            Apple_blog_title = article.text
            return  apple_link, Apple_blog_title

        if process_type == 5:  # 爬取nvida link&title
            target_link = "https://blogs.nvidia.com/ai-podcast/"
            target_text = "AI Podcast"
            ul_elems = soup.find_all('ul')
            all_links = []
            # Extract links and texts from all <ul> elements
            for ul_elem in ul_elems:
                links = [(link.get('href'), link.text) for link in ul_elem.find_all('a')]
                all_links.extend(links)
            # Extract the first link and text after the specified link-text pair
            found = False
            for link, text in all_links:
                # print("text1 is", text)
                if found:
                    return link, text
                if link == target_link and text == target_text:
                    found = True

        if process_type == 6:  # 爬取aws link&title
            articles = soup.find_all('div', class_='lb-col lb-mid-18 lb-tiny-24')
            if not articles:
                print("No articles found.")
                return None, None
            title = articles[0].find('h2').text
            link = articles[0].find('a')['href']
            return  link, title
            
        if process_type == 7:  # 爬取microsoft link&title
            # 由于网站可能有多个这样的链接，我们只选择第一个匹配的项
            link_element = soup.find(tag_name, class_=class_name)
            if link_element:
                text_content = link_element.h3.text.strip()
                href_link = link_element['href']
                return  href_link, text_content
            else:
                return None, None

        # TODO --连接问题，timeout
        if process_type == 8:  # 爬取techcrunch link&title
            # 由于网站可能有多个这样的链接，我们只选择第一个匹配的项
            articles = soup.select('.post-block__title a')
            data_mrf_link, h_title = articles[0]['href'], articles[0].text
            return  data_mrf_link, h_title
        else:
            return None, None
            
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None

# 使用内置报的函数
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
    # Initialize GNews
    google_news = GNews(language=language, country=country, period=period, start_date=start_date, end_date=end_date,
                        max_results=max_results, exclude_websites=exclude_websites)
    # Fetch news based on the query
    news_items = google_news.get_news(query)
    print(news_items)
    # Extract URLs
    urls = [item['url'] for item in news_items]
    content['title'] = [item['title'] for item in news_items]
    for url in urls:
        content['url'].append(url)
        # content['summary'].append(summarize_website_content(url))
    return content
