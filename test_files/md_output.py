import markdown
import pickle
class Source(object):
    def __init__(self, name):
        self.name = name
        self.ori_link = []
        self.url_link = []

        self.title = []
        self.trans_title = []
        
        self.content = []
        self.trans_content = []
    
    def get_page(self, url_link, title):
        self.url_link.append(url_link)
        self.title.append(title)

    def get_content(self, content):
        self.content.append(content)

    def get_trans_info(self, trans_title, trans_content):
        self.trans_title.append(trans_title)
        self.trans_content.append(trans_content)

# 从文件中加载实例
with open('/home/Richard/wangxi/MedAI-News-Podcast/test_files/source_instance.pkl', 'rb') as f:
    news_items = pickle.load(f)

def generate_html_snippet(link, title, keys, content):
    markdown_part = ''
    html_snippet = (
        f"<a href=\"{link}\" style=\"color: #2859C0; text-decoration: none; "
        f"font-size: 14px; font-weight: bold; font-family: Arial;\"> {title}</a>"
        f"<span style=\"margin-left: 5px; background-color: white; padding: 0px 7px; border: 1px solid rgb(251, 88, 88); "
        f"border-radius: 11px; font-size: 10px; color: rgb(251, 88, 88)\">{keys}</span>\n\n"
    )
    
    markdown_part += html_snippet
    markdown_part += f"<span style='font-size: 14px; font-family: news-romans;'>{content}</span>\n\n"
    return markdown_part

def generate_md_summary(news_items, language):
    # 使用加载的实例
    markdown_all = " "
    markdown_all += """<h1 style="color: black; text-align: center; margin-top: 50px;"> <span style='color: #FF4B4B; font-size: 1.25em;'> Med-AI News</span> Podcast</h1>\n\n"""
    markdown_all += """Summary from each sourses\n\n"""
                    
    for keys in news_items:
        print({keys})
        # markdown_all += f"## From: {keys}\n"
        for ii, _ in enumerate(news_items[keys].title):
            print("ii:", ii)
            print("_:", _)
            if language == 'English':
                link = news_items[keys].url_link[ii]
                title = news_items[keys].title[ii]
            # TODO -- 待整理
            else:
                link = news_items[keys].url_link[ii]
                title = news_items[keys].trans_title[ii]
                content = news_items[keys].trans_content[ii]
                markdown_all += generate_html_snippet(link, title, keys, content)

    with open('md_output.md', 'w', encoding='utf-8') as file:
        file.write(markdown_all)
        print("Markdown文件已生成：md_output.md")

    return

generate_md_summary(news_items, "Chinese")

# def generate_md_summary(news_items, language):
#     # 使用加载的实例
#     markdown_all = " "
#     markdown_all += """<h1 style="color: black; text-align: center; margin-top: 50px;"> <span style='color: #FF4B4B; font-size: 1.25em;'> Med-AI News</span> Podcast</h1>\n\n"""
#     markdown_all += """Summary from each sourses\n\n"""
                    
#     for keys in news_items:
#         print({keys})
#         # markdown_all += f"## From: {keys}\n"
#         for ii, _ in enumerate(news_items[keys].title):
#             if language == 'English':
#                 link = news_items[keys].url_link[ii]
#                 title = news_items[keys].title[ii]

#                 html_snippet = (
#                     f"<a href=\"{link}\" style=\"color: #2859C0; text-decoration: none; "
#                     f"font-size: 14px; font-weight: bold; font-family: Arial;\"> {title}</a>"
#                     f"<span style=\"margin-left: 5px; background-color: white; padding: 0px 7px; border: 1px solid rgb(251, 88, 88); "
#                     f"border-radius: 11px; font-size: 10px; color: rgb(251, 88, 88)\">{keys}</span>\n\n"
#                 )

#                 markdown_all += html_snippet
#                 markdown_all += f"<span style=\'font-size: 14px; font-family: news-romans;'>{news_items[keys].content[ii]}</span>\n\n"

#             # TODO -- 待整理
#             else:
#                 link = news_items[keys].url_link[ii]
#                 title = news_items[keys].trans_title[ii]

#                 html_snippet = (
#                     f"<a href=\"{link}\" style=\"color: #2859C0; text-decoration: none; "
#                     f"font-size: 14px;font-weight: bold;\"> {title}</a>"
#                     f"<span style=\"margin-left: 5px; background-color: white; padding: 0px 7px; border: 1px solid rgb(251, 88, 88); "
#                     f"border-radius: 10px; font-size: 12px; color: rgb(251, 88, 88)\">{keys}</span>\n\n"
#                 )

#                 markdown_all += html_snippet
#                 markdown_all += f" {news_items[keys].trans_content[ii]}\n\n"

#     with open('md_output.md', 'w', encoding='utf-8') as file:
#         file.write(markdown_all)
#         print("Markdown文件已生成：md_output.md")

#     return

