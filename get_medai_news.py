import requests
import arxiv
from bs4 import BeautifulSoup

from gnews import GNews
# from newspaper import Config
# from pytube import Playlist
from youtubesearchpython import Playlist, playlist_from_channel_id

from utils import unify_time, check_date_match, \
    extract_text_from_pdf, find_educational_institutions, \
    strtime2date, select_news_items


def get_websit_info(url, tag_name, class_name, process_type, local_time, day):
    # 使用requests和beautifulsoup的函数
    # Make a request to a web page, and return the status code
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }

    response = requests.get(url, headers=headers) 
    
    # TODO: delete or not
    web_time = ''

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
            
            # TODO: check the articles and web_time are exist
            web_time = unify_time(web_time)
            
            if check_date_match(web_time, local_time, day) == True:
                if articles:                
                    web_titile = articles.get('alt')
                    web_link = url + articles.get('href')

                else:
                    print("Couldn't find the target post URL.")
                    raise ValueError  
            else:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None
                process_type = None


        # 爬取paper with code信息
        elif process_type == "paperwithcode":  
            articles = soup.find(class_=class_name).find('h1')
            # TODO --0104有报错需要修改位置
            # web_time = soup.find(class_=class_name).find('span', class_='author-name-text item-date-pub').get_text()
            web_time = "20240104"
            # TODO: check the articles and web_time are exist
            web_time = unify_time(web_time)

            if check_date_match(web_time, local_time, day) == True:
                if articles:
                    # 提取 href 值和标题文本
                    web_link = "https://paperswithcode.com" + articles.a['href']
                    web_titile = articles.a.get_text()        
                else:
                    print("Couldn't find the target post URL.")
                    raise ValueError
            else:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None
         
        # auntminnie
        elif process_type == "auntminnie":
            soup = BeautifulSoup(response.content, 'html.parser')   
            a_tag = soup.find(class_=class_name).find(tag_name)
            web_link = url + a_tag.get('href')
            web_titile  = a_tag.get_text()
            
            # 获取时间
            response = requests.get(web_link, headers=headers)
            # response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.content, 'html.parser')
            web_time = soup.find(class_="author-published-node__content-published").get_text()
            web_time = unify_time(web_time)
            if check_date_match(web_time, local_time, day) is not True:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None
        
        # mobi
        elif process_type == "mobihealthnews":
            soup = BeautifulSoup(response.content, 'html.parser')
            web_time = soup.find('div', class_='views-field views-field-created-1').get_text(strip=True)
            web_time = unify_time(web_time)
            
            if check_date_match(web_time, local_time, day) == True:
                a_tag = soup.find(class_=class_name).find(tag_name)
                web_link = url + a_tag.get('href')
                print("mobi web_link here:", web_link)
                web_titile = a_tag.get_text()
                web_time = unify_time(web_time)
            else:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None

        '''
        # TODO: erroe here
        # natureBME
        elif process_type == "natureBME" :
            soup = BeautifulSoup(response.content, 'html.parser') 
            output_test_nature =  str(response.content) 
            web_time = "2024-01-24"
            # web_time = soup.find('div', class_="c-article-header")
            print("natureBME time:", web_time)

            if check_date_match(web_time, local_time, day) == True:
                a_tag = soup.find(class_=class_name).find(tag_name)
                web_link = url + a_tag.get('href')
                a_tag = soup.find(class_=class_name).find(tag_name)
                web_link = a_tag.get('href')
                web_titile = a_tag.get_text()
        
            else:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None
        '''

        return web_link, web_titile, web_time 

    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        raise ValueError
        


def get_arxiv_summary(_arxiv, query, trigger_time, day, max_results):
    # 1. Construct the default API client.
    # Search for recent articles matching the query"
    client = arxiv.Client()    
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = client.results(search)

    # 2. 读取config_qs_university大学排名
    university_500_list = []
    with open('config_qs_university.txt', 'r') as f:
        for line in f:
            university_500_list.append(line.strip().lower()) 

    # 3. select valuable papers by date and qs ranking
    # debug
    output_list = []
    # debug end 
    selected_items = []
    selected_idx = []
    for result in results:
        if check_date_match(result.updated, trigger_time, day) == True:
            # get institution messages
            pdf_text = extract_text_from_pdf(result.pdf_url)
                    
            # 调用函数并尝试获取pdf里的机构字符串，但是会存在没有机构名字的paper
            # TODO: 法语、西语等非英语，关键词的匹配语法需要增加
            institution_text = find_educational_institutions(pdf_text)
            
            # 检查 institution_text 是否为 None
            if institution_text is None:
                print("There is a paper can't find institution")
                print(result.pdf_url)
                print('!!!!!!!!!!')
                continue  # 如果是 None，跳过当前循环的剩余部分
            
            # 将文本转换为小写
            institution_text = institution_text.lower()

            # 按照 university_500_list 的顺序检查每个大学名称是否出现在 institution_text 中
            # TODO 顺序还没有实现
            for _index, university in enumerate(university_500_list):
                if university in institution_text:
                    selected_items.append(result)
                    selected_idx.append(_index)
                    # print("first match institution is :", university)
                    break
            
            '''# debug
            entry = {
                "[title]" : result.title,
                "[author.name]": result.authors,
                "[category]": result.categories,
                "[arxiv:primary_category]": result.primary_category,
                "[arxiv:institution_text]": institution_text,
                "[arxiv:selected_idx]": _index,
                "[arxiv:summary]": result.summary,
                "[arxiv:journal_pdf]": result.pdf_url          
            }
            output_list.append(entry)
            # debug end '''
        else:
            break
    
    '''# debug 
    import pandas as pd
    file_path = "/home/medai/wangxi/MedAI-News-Podcast/test/arxiv_institution_test_" + trigger_time + ".xlsx"
    df = pd.DataFrame(data=output_list).set_index(["[title]"])
    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer) 
    print(f'arxiv测试已成功保存到文件:{file_path}')
    # debug end '''

    # 4. sort the selected papers
    if len(selected_items) > 0:
        sorted_lists = sorted(zip(selected_idx, selected_items))
        selected_idx, selected_items = zip(*sorted_lists)    
        
        publisher = "Arxiv"
        for _index, result in enumerate(selected_items):
            # only keep the first 4 papers
            if _index > 3:
                break
            web_time = unify_time(str(result.published))    
            _arxiv.get_page(result.entry_id, result.title, web_time, publisher)
            # print("result:", result)
    else:
        print("arxiv get nothing, you may want to try it later!")

    return


def fetch_gnews_links(_google, query, trigger_time, day, max_results=3):
    # use google engine to search news
    end_date, start_date = strtime2date(trigger_time, day)
    google_news = GNews(language='en', 
                        start_date=start_date, end_date=end_date,
                        max_results=max_results, exclude_websites=None)
          
    # 根据query获取新闻
    news_items = google_news.get_news(query)
    # 根据topic获取新闻
    # news_items = google_news.get_news_by_topic('HEALTH')
    
    if news_items == []:
        print("ERROR: can't get google news")   
    else:
        publisher_list = []
        with open('config_google_publisher.txt', 'r') as f:
            for line in f:                
                publisher_list.append(line.strip()) # 去除每行的换行符并添加到列表中

        best_google_news = select_news_items(publisher_list, news_items)
        # print("筛选出的google news are:", best_google_news)

        # TODO: 因为无法download页面，可能无法load3个新闻
        for gn in best_google_news:
            try:
                web_time = unify_time(gn.get('published date'))
                article = google_news.get_full_article(gn['url'])
                _google.get_content(article.text)
                _google.get_page(gn.get('url'), article.title, web_time, gn['publisher']['title'])
                # _arxiv.get_content(result.summary)
                import pdb; pdb.set_trace()
            except Exception as e:
                print(f"Error retrieving full article for {gn['url']}: {e}")
                # 处理下一条新闻
                continue

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

