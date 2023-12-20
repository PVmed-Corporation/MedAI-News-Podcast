import markdown
import pickle

# # 从文件中加载实例
# with open('source_instance_cn.pkl', 'rb') as f:
#     news_items = pickle.load(f)

def generate_md_summary(news_items, language):
    # 使用加载的实例
    markdown_all = " "
    markdown_all += """<h1 style="color: black; text-align: center; margin-top: 50px;"> <span style='color: #FF4B4B; font-size: 1.25em;'> Med-AI News</span> Podcast</h1>\n\n"""
    markdown_all += """Summary from each sourses\n\n"""
                    
    for keys in news_items:
        print({keys})
        # markdown_all += f"## From: {keys}\n"
        for ii, _ in enumerate(news_items[keys].title):
            if language == 'English':
                link = news_items[keys].url_link[ii]
                title = news_items[keys].title[ii]

                html_snippet = (
                    f"<a href=\"{link}\" style=\"color: #2859C0; text-decoration: none; "
                    f"font-size: 14px; font-weight: bold; font-family: Arial;\"> {title}</a>"
                    f"<span style=\"margin-left: 5px; background-color: white; padding: 0px 7px; border: 1px solid rgb(251, 88, 88); "
                    f"border-radius: 11px; font-size: 10px; color: rgb(251, 88, 88)\">{keys}</span>\n\n"
                )

                markdown_all += html_snippet
                markdown_all += f"<span style=\'font-size: 14px; font-family: news-romans;'>{news_items[keys].content[ii]}</span>\n\n"

            # TODO -- 待整理
            else:
                link = news_items[keys].url_link[ii]
                title = news_items[keys].trans_title[ii]

                html_snippet = (
                    f"<a href=\"{link}\" style=\"color: #2859C0; text-decoration: none; "
                    f"font-size: 14px;font-weight: bold;\"> {title}</a>"
                    f"<span style=\"margin-left: 5px; background-color: white; padding: 0px 7px; border: 1px solid rgb(251, 88, 88); "
                    f"border-radius: 10px; font-size: 12px; color: rgb(251, 88, 88)\">{keys}</span>\n\n"
                )

                markdown_all += html_snippet
                markdown_all += f" {news_items[keys].trans_content[ii]}\n\n"

    with open('md_output.md', 'w', encoding='utf-8') as file:
        file.write(markdown_all)
        print("Markdown文件已生成：md_output.md")

    return

