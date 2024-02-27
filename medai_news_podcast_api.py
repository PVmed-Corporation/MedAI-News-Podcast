# encoding:utf-8
from getnews.get_medai_news import get_websit_info
from getnews.get_news_third import get_arxiv_summary, \
    get_youtube_dojo, fetch_gnews_links
from summarize.summarize_medai_news import LLM_processing_content, generate_paper_summary
from openai import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from exhibit.generate_output import generate_result
import time


class Source(object):
    def __init__(self, name):
        self.name = name
        self.ori_link = []
        self.url_link = []
        self.web_time = []
        self.publisher = []

        self.title = []
        self.trans_title = []
        
        self.content = []
        self.trans_content = []
    
    def get_page(self, url_link, title, web_time, publisher):
        self.url_link.append(url_link)
        self.title.append(title)
        self.web_time.append(web_time)
        self.publisher.append(publisher)

    def get_content(self, content):
        self.content.append(content)

    def get_trans_info(self, trans_title, trans_content):
        self.trans_title.append(trans_title)
        self.trans_content.append(trans_content)


def medai_news_podcast_api(websites, token_path, language, output_folder, output_format, trigger_time, day):  
    # 1. collect the information
    news_items = {}

    # arxiv直接调用api
    query =  "(ti:medical AND cat:eess.IV) OR (ti:medical AND cat:cs.CV) OR (ti:medical AND cat:cs.AI) OR "\
             "(ti:image AND cat:eess.IV) OR (ti:image AND cat:cs.CV) OR (ti:image AND cat:cs.AI)"
    # query =  '("image" AND "medical") OR ("medical" AND eess.IV) OR ("MRI" AND eess.IV) OR ("CT" AND eess.IV) OR ("medical" AND cs.CV) OR ("medical image" AND cs.AI) OR ("clinical" AND cs.CV) OR ("clinical" AND eess.IV) OR ("ai" AND "medical") OR "image segentation"' 
    # query =  '("image" AND "medical") OR ("medical" AND eess.IV) OR ("medical" AND cs.CV) OR ("clinical image" AND cs.CV)'
    # query = "Liver tumor segmentation OR ('tumor' AND (cs.CV OR eess.IV))"

    _arxiv = Source("arxiv")
    get_arxiv_summary(_arxiv, query, trigger_time, day, max_results=30)
    if len(_arxiv.title) > 0:
        news_items["arxiv"] = _arxiv
    
    # google news
    query = "AI medical, medical imaging"
    # query = "AI medical, clinical image technology, medical image, AI"
    # query = "MRI AI"

    _google = Source("google")
    fetch_gnews_links(_google, query, trigger_time, day, max_results=10)
    if len(_google.title) > 0:
        news_items["google"] = _google
    
    # # TODO --YOUTUBE上的内容只对视频界面的文字做了归纳，没有调用字幕归纳的函数
    # channel_id = "UCMLtBahI5DMrt0NPvDSoIRQ"
    # _youtb = Source("youtube")
    # get_youtube_dojo(_youtb, channel_id)
    # news_items["youtube"] = _youtb

    # 遍历网站信息列表并获取信息
    for site in websites:
        # TODO: 按照最新内容，可能不止一个link
        web_link, web_title, web_time = get_websit_info(site.url, site.tag_name, site.class_name, site.process_type, trigger_time, day)
        if web_link is not None:
            _web = Source(site.process_type)
            _web.get_page(web_link, web_title, web_time, site.process_type)
            news_items[site.process_type] = _web

            print(f"在{site.process_type}网站爬取到的link和title和time是:\n{web_link}: {web_title}\n 发布时间是: {web_time}\n")

    # --------------------------------------------------------------------------------------------
    # 2. summarize the content
    with open(token_path) as f:
            private_token = f.readline()
    client = OpenAI(api_key=private_token)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", openai_api_key=private_token)
    
    # 生成每篇文章的summary
    LLM_processing_content(llm, client, news_items, language)
    
    # 修改messages中的内容部分为全部网页的summary
    summary_whole = [] # [item['web_summarize'] for item in news_items]

    for keys in news_items:
        print("info from:", keys)
        for ii, _ in enumerate(news_items[keys].title):
            print(ii)
            # print("url:", news_items[keys].url_link[ii])
            # update summary
            if keys in ["arxiv","auntminnie","机器之心","google"]:
                summary_whole.append(news_items[keys].content[ii])

            if language == 'English':
                print("title:", news_items[keys].title[ii])
                print("web_time:", news_items[keys].web_time[ii])
                print("web_summarize:", news_items[keys].content[ii])
            else:
                print("title:", news_items[keys].trans_title[ii])
                print("web_time:", news_items[keys].web_time[ii])
                print("web_summarize:", news_items[keys].trans_content[ii])
        
    # 提取所有信息里面的关键放在开头
    LLM_paper_summary = generate_paper_summary(client, summary_whole, language)
    print("LLM_paper_summary: \n", LLM_paper_summary)

    # -----------------------------------------------------------------------------------
    # 3. generate the podcast to markdown file
    if output_format == 'excel':
        output_file_path = output_folder + language + '_'+ trigger_time + '_output.xlsx'
    else:
        output_file_path = output_folder + language + '_'+ trigger_time + '_output.md'

    generate_result(news_items, language, LLM_paper_summary, output_format, output_file_path)

    return


if __name__ == '__main__':
    # 定义要爬取的网站信息
    from collections import namedtuple
    WebsiteInfo = namedtuple('WebsiteInfo', ['url', 'tag_name', 'class_name', 'process_type'])

    # 这里是可以一步获取标题和链接的
    # 如果链接太多会 too many values to unpack (expected 2)
    websites = [
        # WebsiteInfo(url="https://www.jiqizhixin.com", tag_name="a", class_name="article-item__right", process_type="机器之心"), # 机器之心
        # WebsiteInfo(url="https://paperswithcode.com/latest", tag_name="h1", class_name="col-lg-9 item-content", process_type="paperwithcode"), # paper with code
        # WebsiteInfo(url="https://www.auntminnie.com/", tag_name="a", class_name="node__title", process_type="auntminnie"), # auntminnie
        # # WebsiteInfo(url="https://www.mobihealthnews.com/", tag_name="a", class_name="views-field views-field-field-short-headline views-field-title news", process_type="mobihealthnews"), # mobihealthnews
        # TODO --添加分词器
        # WebsiteInfo(url="https://www.nature.com/natbiomedeng/", tag_name="a", class_name="c-hero__title u-mt-0", process_type="natureBME"), # natureBME
        # WebsiteInfo(url="https://machinelearning.apple.com/", tag_name="h3.post-title a", class_name="", process_type="apple"), # apple_link&title
        # WebsiteInfo(url="https://blogs.nvidia.com/ai-podcast/", tag_name="ul", class_name="AI Podcast",process_type="nvidia"), # nvida_link&title
        # WebsiteInfo(url="https://aws.amazon.com/blogs/machine-learning/", tag_name="div", class_name="lb-col lb-mid-18 lb-tiny-24", process_type="aws"), # aws
        # WebsiteInfo(url="https://blogs.microsoft.com/", tag_name="a", class_name="f-post-link", process_type="microsoft"), # microsoft
        # WebsiteInfo(url="https://openai.com/", tag_name="a", class_name="ui-link group relative cursor-pointer", process_type="openai"), # openai_link
        # WebsiteInfo(url="https://techcrunch.com/category/artificial-intelligence/", tag_name="", class_name="", process_type="techcrunch"), # techcrunch频道
        # # TODO  Error code: 400
        # # WebsiteInfo(url="https://le4ews xfridman.com/podcast/", tag_name="a", class_name="", process_type="lexfridman") # lexfridman_lin
    ]
    
    # 2. api token text path
    token_path = "config_file.txt"
    
    # 3. language可以选择Chinese或English
    language =  'Chinese'
    
    # 4. output_folder选择一个文件夹
    output_folder =  '/home/medai/songfeng/songfeng_output/'
    
    # 5. output format 可选markdown, markdown_dingding或excel
    output_format = 'markdown_dingding'
    
    # 6. the local time when we run the code
    # check the time zone where you are or set the time you want to get
    trigger_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    # trigger_time = '2024-02-28-05-59-59'
    
    # 7. day 可选today和yesterday
    day = "yesterday"
    
    medai_news_podcast_api(websites, token_path, language, output_folder, output_format, trigger_time, day)

