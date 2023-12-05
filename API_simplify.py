from reptile_func_simplify import *
from collections import namedtuple

# 定义要爬取的网站信息
WebsiteInfo = namedtuple('WebsiteInfo', ['url', 'tag_name', 'class_name', 'process_type'])

#这里是可以一步获取标题和链接的
#如果链接太多会 too many values to unpack (expected 2)
websites = [
    WebsiteInfo(url="https://machinelearning.apple.com/", tag_name="", class_name="", process_type=4), #Apple_link&title
    WebsiteInfo(url="https://blogs.nvidia.com/ai-podcast/", tag_name="", class_name="",process_type=5), #nvida_link&title
    WebsiteInfo(url="https://aws.amazon.com/blogs/machine-learning/", tag_name="a", class_name="card-tile", process_type=6), #aws
 ]

# 遍历网站信息列表并获取信息
for site in websites:
    web_link, web_title = get_info(site.url, site.tag_name, site.class_name, site.process_type)

    print(f"在{site.url}网站爬取到的link和title是：\n{web_link}: {web_title}\n")


#这里是不可以一步获取标题和链接的
#openai_link(1205早上openai这个网址连接不稳定，经常连不上可能需要注释掉)
url = "https://openai.com"
blog_url = f"{url}/blog"
tag_name = "a"
class_name = "ui-link group relative cursor-pointer"
process_type = 1
openai_blog_url = get_info(url, tag_name, class_name, process_type) #找到链接

#openai_title
url = openai_blog_url
tag_name = "h1",
class_name = "f-display-2"
process_type = 2
openai_title = get_info(url, tag_name, class_name, process_type)
print("在https://openai.com网站爬取到的link和title是：", "\n", openai_blog_url,":", openai_title, "\n")

#lexfridman_link
url = "https://lexfridman.com/podcast/"
process_type = 3
tag_name = ""
class_name = ""
L_link = get_info(url, tag_name, class_name, process_type)

#lexfridman_title
url = L_link
tag_name = "h1"
class_name = "entry-title"
process_type = 2
lexfridman_title = get_info(url, tag_name, class_name, process_type)
print("在https://lexfridman.com/podcast/网站爬取到的link和title是：","\n", L_link,":", lexfridman_title, "\n")

#后面生成页面并没有用到arxiv，也没有找到title的获取
arxiv_summary = get_arxiv_summary()
print("arxiv_summary:", arxiv_summary)
#mtechcrunch 用户将无法从中国大陆使用 Yahoo 的产品
#youtube上的Machine Learning Dojo with Tim Scarfe的视频因连接问题爬取不到
