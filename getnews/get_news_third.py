import arxiv
from gnews import GNews
# from newspaper import Config
# from pytube import Playlist
from youtubesearchpython import Playlist, playlist_from_channel_id

from utils import unify_time, check_date_match, \
    extract_text_from_pdf, find_educational_institutions, \
    strtime2date, select_news_items


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
    with open('config/config_qs_university.txt', 'r') as f:
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
    # google_news = GNews(language='zh-Hans', country='CN', period='1d',
    #                     start_date=None, end_date=None,
    #                     max_results=max_results, exclude_websites=None)
    # 根据query获取新闻
    news_items = google_news.get_news(query)
    # 根据topic获取新闻
    # news_items = google_news.get_news_by_topic('HEALTH')
    
    if news_items == []:
        print("ERROR: can't get google news")   
    else:
        publisher_list = []
        with open('config/config_google_publisher.txt', 'r') as f:
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

