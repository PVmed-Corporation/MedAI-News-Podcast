from get_medai_news import get_websit_info, get_arxiv_summary, get_youtube_dojo, fetch_gnews_links
from summary_simplify_test import summarize, completion, LLM_processing_content, generate_paper_summary

def medai_news_podcast_api(websites):
    # 1. collect the information
    # 遍历网站信息列表并获取信息
    news_items = [ ]
    # 1208新增部分
    for site in websites:
        web_link, web_title = get_websit_info(site.url, site.tag_name, site.class_name, site.process_type)
        new_web_link = {'web': site.url, 'url': web_link, 'title': web_title} # 'url'指的是文章的地址
        news_items.append(new_web_link)
        print(f"在{site.url}网站爬取到的link和title是:\n{web_link}: {web_title}\n")

    # 后面生成页面并没有用到arxiv，也没有找到title的获取
    arxiv_summary = get_arxiv_summary()
    print("arxiv_summary:", arxiv_summary)

    # # TODO -- 连接问题，timeout
    # # youtube上的Machine Learning Dojo with Tim Scarfe的视频因连接问题爬取不到
    # youtube_content = get_youtube_dojo()
    # print("youtube_content:", youtube_content)

    # TODO -- 连接问题，返回空值
    # googlenews也不行
    google_news = fetch_gnews_links(query='AI, LLM, Machine learning', max_results = 4)
    print("google_news:", google_news)

    # 2. summarize the content
    # 生成内容部分
    LLM_content = LLM_processing_content(news_items)
    print("LLM_content:", LLM_content)
    # 生成整体的summary部分
    LLM_paper_summary = generate_paper_summary(LLM_content)
    print("LLM_paper_summary: ", LLM_paper_summary)

    # 3. generate the podcast

    return 


if __name__ == '__main__':
    # 定义要爬取的网站信息
    from collections import namedtuple
    WebsiteInfo = namedtuple('WebsiteInfo', ['url', 'tag_name', 'class_name', 'process_type'])

    # 这里是可以一步获取标题和链接的
    # 如果链接太多会 too many values to unpack (expected 2)
    websites = [
        WebsiteInfo(url="https://machinelearning.apple.com/", tag_name="h3.post-title a", class_name="", process_type="apple"), # apple_link&title
        WebsiteInfo(url="https://blogs.nvidia.com/ai-podcast/", tag_name="ul", class_name="AI Podcast",process_type="nvidia"), # nvida_link&title
        WebsiteInfo(url="https://aws.amazon.com/blogs/machine-learning/", tag_name="div", class_name="lb-col lb-mid-18 lb-tiny-24", process_type="aws"), # aws
        WebsiteInfo(url="https://blogs.microsoft.com/", tag_name="a", class_name="f-post-link", process_type="microsoft"), # microsoft
        WebsiteInfo(url="https://openai.com/", tag_name="a", class_name="ui-link group relative cursor-pointer", process_type="openai"), # openai_link
        WebsiteInfo(url="https://lexfridman.com/podcast/", tag_name="a", class_name="", process_type="lexfridman"), # lexfridman_link
        # TODO --连接问题，timeout
        # WebsiteInfo(url="https://techcrunch.com/category/artificial-intelligence/", tag_name="", class_name="", process_type="techcrunch"), # techcrunch频道
    ]

    medai_news_podcast_api(websites)

