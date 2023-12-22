# 使用pandas输出内容
# 循环添加条目到列表中
import pandas as pd
def generate_df_summary(news_items, language):
    output_list = []
    for keys in news_items:
        for ii, _ in enumerate(news_items[keys].title):
            if language == 'English':
                entry = {
                    'From': keys,
                    'Title': news_items[keys].title[ii],
                    'URL': news_items[keys].url_link[ii],
                    'Web_Summary': news_items[keys].content[ii]
                }
            else:
                entry = {
                    'From': keys,
                    'Title': news_items[keys].trans_title[ii],
                    'URL': news_items[keys].url_link[ii],
                    'Web_Summary': news_items[keys].trans_content[ii]
                }                        
            output_list.append(entry)

    # 将列表转换为DataFrame
    df = pd.DataFrame(data=output_list).set_index(["From","Title"])
    with pd.ExcelWriter("web_sum_output.xlsx") as writer:
        df.to_excel(writer) 
    print(df)
    return

# 使用 exec() 函数执行文件中的代码，将其中定义的变量导入到当前的命名空间中
exec(open('news_items.py').read())

# 现在你可以使用 news_items 这个变量来访问你保存的字典数据
for key, value in news_items.items():
    print(f"Key: {key}")
    print(f"Value: {value}")
    # 在这里进行你的处理

def generate_md_summary(news_items, LLM_paper_summary, language):
    # 使用加载的实例
    markdown_all = " "
    markdown_all += """<h1 style="color: black; text-align: center; margin-top: 50px;"> <span style='color: #FF4B4B; font-size: 1.25em;'> Med-AI News</span> Podcast</h1>\n\n"""
    markdown_all += """## Key Points of Today News\n\n"""
    markdown_all += LLM_paper_summary + '''\n\n'''

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
                    f"border-radius: 11px; font-size: 10px; color: rgb(251, 88, 88)\">{keys}</span>\n\n"
                )

                markdown_all += html_snippet
                markdown_all += f" {news_items[keys].trans_content[ii]}\n\n"

    with open('md_output.md', 'w', encoding='utf-8') as file:
        file.write(markdown_all)
        print("Markdown文件已生成：md_output.md")

    return

