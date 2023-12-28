# encoding:utf-8
from get_medai_news import get_websit_info, get_arxiv_summary, \
    get_youtube_dojo, fetch_gnews_links
from summarize_medai_news import LLM_processing_content, generate_paper_summary
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from generate_output import generate_result
import time


class Source(object):
    def __init__(self, name):
        self.name = name
        self.ori_link = []
        self.url_link = []

        self.title = []
        self.trans_title = []
        
        self.web_time = []

        self.content = []
        self.trans_content = []
    
    def get_page(self, url_link, title, web_time):
        self.url_link.append(url_link)
        self.title.append(title)
        self.web_time.append(web_time)

    def get_content(self, content):
        self.content.append(content)

    def get_trans_info(self, trans_title, trans_content):
        self.trans_title.append(trans_title)
        self.trans_content.append(trans_content)


def medai_news_podcast_api(websites, token_path, language, output_folder, format):

    with open(token_path) as f:
            private_token = f.readline()

    # 1. collect the information
    news_items = {}
    
    # # google news
    query = "medical imaging news OR medical AND image processing technology)"

    # query = "(medical imaging, AI) OR (MRI AND image processing technology) OR (medicine AND imaging)"
    
    _google = Source("google")
    fetch_gnews_links(_google, query, max_results=5) # max_results可以自由改动
    news_items["google"] = _google
    
    # # # arxiv直接调用api
    # _arxiv = Source("arxiv")
    # query =  '(medical AND eess.IV) OR ("MRI" AND eess.IV) OR ("CT" AND eess.IV) OR ("medical" AND cs.CV) OR ("medical image" AND cs.AI)' 

    # get_arxiv_summary(_arxiv, query, max_results=7) # max_results可以自由改动
    # news_items["arxiv"] = _arxiv
    '''
    attempts = 2
    while attempts > 0:
        result = get_arxiv_summary(_arxiv, query, max_results=5)
        print("1 arxiv result:", result)
        if result is not None:
            # 如果结果不是 None, 则打印结果并跳出循环
            print("2 arxiv result:", result)
            break
        # 如果结果是 None, 则等待 2 秒再尝试获取
        print("3 arxiv result:", result)
        time.sleep(1)
        attempts -= 1
    '''
    
    # # TODO --YOUTUBE上的内容好像只对视频界面的文字做了归纳，没有调用字幕归纳的函数
    # channel_id = "UCMLtBahI5DMrt0NPvDSoIRQ"
    # _youtb = Source("youtube")
    # get_youtube_dojo(_youtb, channel_id)
    # news_items["youtube"] = _youtb

    # 遍历网站信息列表并获取信息
    for site in websites:
        # TODO: 按照最新内容，可能不止一个link
        web_link, web_title, web_time = get_websit_info(site.url, site.tag_name, site.class_name, site.process_type)

        _web = Source(site.process_type)
        _web.get_page(web_link, web_title, web_time)

        news_items[site.process_type] = _web

        print(f"在{site.process_type}网站爬取到的link和title和time是:\n{web_link}: {web_title}\n 发布时间是: {web_time}\n")

    # 2. summarize the content
    client = OpenAI(api_key=private_token)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", openai_api_key=private_token)
    
    # 生成每篇文章的summary
    LLM_processing_content(llm, client, news_items, language)
    
    # 修改messages中的内容部分为全部网页的summary
    summary_whole = [] # [item['web_summarize'] for item in news_items]
    
    for keys in news_items:
        print("info from:", keys)
        print("info news_items[keys].title:", news_items[keys].title)
        '''
        # Check the lengths of the lists
        title_len = len(news_items[keys].title) if hasattr(news_items[keys], 'title') else 0
        trans_title_len = len(news_items[keys].trans_title) if hasattr(news_items[keys], 'trans_title') else 0
        web_time_len = len(news_items[keys].web_time) if hasattr(news_items[keys], 'web_time') else 0
        content_len = len(news_items[keys].content) if hasattr(news_items[keys], 'content') else 0
        trans_content_len = len(news_items[keys].trans_content) if hasattr(news_items[keys], 'trans_content') else 0
        
        print("Length of title:", title_len)
        print("Length of trans_title:", trans_title_len)
        print("Length of web_time:", web_time_len)
        print("Length of content:", content_len)
        print("Length of trans_content:", trans_content_len)

        '''
        for ii, _ in enumerate(news_items[keys].title):
            print(ii)
            # print("url:", news_items[keys].url_link[ii])
            # update summary
            if keys in ["arxiv","auntminnie","机器之心", "google"]:
                summary_whole.append(news_items[keys].content[ii])

            if language == 'English':
                print("title:", news_items[keys].title[ii])
                print("web_time:", news_items[keys].web_time[ii])
                print("web_summarize:", news_items[keys].content[ii])
            else:
                print("title:", news_items[keys].trans_title[ii])
                print("web_time:", news_items[keys].web_time[ii])
                print("web_summarize:", news_items[keys].trans_content[ii])
        
    # # 提取所有信息里面的关键放在开头
    # LLM_paper_summary = generate_paper_summary(client, summary_whole, language)
    # print("LLM_paper_summary: \n", LLM_paper_summary)

    # # 3. generate the podcast
    # # 生成markdown文件
    # _time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    # if format == 'excel':
    #     output_file_path = output_folder + language + '_'+ _time + '_output.xlsx'
    # else:
    #     output_file_path = output_folder + language + '_'+ _time + '_output.md'
    # generate_result(news_items, language, LLM_paper_summary, format, output_file_path)
    
    # return


if __name__ == '__main__':
    # 定义要爬取的网站信息
    from collections import namedtuple
    WebsiteInfo = namedtuple('WebsiteInfo', ['url', 'tag_name', 'class_name', 'process_type'])

    # 这里是可以一步获取标题和链接的
    # 如果链接太多会 too many values to unpack (expected 2)
    websites = [
        # WebsiteInfo(url="https://www.jiqizhixin.com/", tag_name="a", class_name="article-item__right", process_type="机器之心"), # 机器之心
        # WebsiteInfo(url="https://paperswithcode.com", tag_name="h1", class_name="col-lg-9 item-content", process_type="paperwithcode"), # paper with code
        # WebsiteInfo(url="https://www.auntminnie.com/", tag_name="a", class_name="node__title", process_type="auntminnie"), # auntminnie
        # WebsiteInfo(url="https://www.mobihealthnews.com/", tag_name="a", class_name="views-field views-field-field-short-headline views-field-title", process_type="mobihealthnews"), # mobihealthnews
        # TODO --添加分词器
        # WebsiteInfo(url="https://www.nature.com/natbiomedeng/", tag_name="a", class_name="c-hero__title u-mt-0", process_type="natureBME") # natureBME
        # WebsiteInfo(url="https://machinelearning.apple.com/", tag_name="h3.post-title a", class_name="", process_type="apple"), # apple_link&title
        # WebsiteInfo(url="https://blogs.nvidia.com/ai-podcast/", tag_name="ul", class_name="AI Podcast",process_type="nvidia"), # nvida_link&title
        # WebsiteInfo(url="https://aws.amazon.com/blogs/machine-learning/", tag_name="div", class_name="lb-col lb-mid-18 lb-tiny-24", process_type="aws"), # aws
        # WebsiteInfo(url="https://blogs.microsoft.com/", tag_name="a", class_name="f-post-link", process_type="microsoft"), # microsoft
        # WebsiteInfo(url="https://openai.com/", tag_name="a", class_name="ui-link group relative cursor-pointer", process_type="openai"), # openai_link
        # WebsiteInfo(url="https://techcrunch.com/category/artificial-intelligence/", tag_name="", class_name="", process_type="techcrunch"), # techcrunch频道
        # # TODO  Error code: 400
        # # WebsiteInfo(url="https://le4ews xfridman.com/podcast/", tag_name="a", class_name="", process_type="lexfridman") # lexfridman_lin
    ]
    
    # language可以选择Chinese或English
    # output_folder选择一个文件夹
    # format可选markdown或excel
    medai_news_podcast_api(websites, "config_file.txt", 'English', 'output/', 'markdown')



