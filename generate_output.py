import pandas as pd


def generate_html_snippet(news_items, keys, language, ):
    markdown_part = ''
    
    for ii, _ in enumerate(news_items[keys].title):
        link = news_items[keys].url_link[ii]
        if language == 'English':
            title = news_items[keys].title[ii]
            content = news_items[keys].content[ii]
            web_time = news_items[keys].web_time[ii]
        else:
            title = news_items[keys].trans_title[ii]
            content = news_items[keys].trans_content[ii]
            web_time = news_items[keys].web_time[ii]
        
        html_snippet = (
            f"### <a href=\"{link}\" style=\"color: #2859C0; text-decoration: none; "
            f"font-size: 15px; font-weight: bold; font-family: Arial;\"> {title}</a>"
            f"<span style=\"margin-left: 5px; background-color: white; padding: 0px 7px; border: 1px solid rgb(251, 88, 88); "
            f"border-radius: 11px; font-size: 10px; color: rgb(251, 88, 88)\">{keys}</span>\n\n"
        )
        
        markdown_part += html_snippet
        markdown_part += f"<span style='font-size: 10px; font-family: news-romans;'>{web_time}</span>\n\n"
        markdown_part += f"<span style='font-size: 14px; font-family: news-romans;'>{content}</span>\n\n"
        
    
    return markdown_part


def generate_result(news_items, language, LLM_paper_summary, format, output_path):
    if format == "excel":
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

        # TODO: yichuqu 将列表转换为DataFrame
        df = pd.DataFrame(data=output_list).set_index(["From","Title"])
        with pd.ExcelWriter(output_path) as writer:
            df.to_excel(writer) 
        print("excel文件已生成: ", output_path) 

    else:
        # 使用加载的实例
        markdown_all = " "
        markdown_all += """<h1 style="color: black; text-align: center; margin-top: 50px;"> <span style='color: #FF4B4B; font-size: 1.25em;'> Med-AI News</span> Podcast</h1>\n\n"""
        markdown_all += """## Key Points of Today's News\n\n"""
        markdown_all += LLM_paper_summary + '''\n\n'''

        # 正文的信息排版
        for ii, keys in enumerate(news_items):
            print(keys,"加入md文件")
            if ii<2:
                markdown_all += f"""## Paper from {keys} \n\n"""
                markdown_all += generate_html_snippet(news_items, keys, language)
            else:
                if ii == 2:
                    markdown_all += """## News from Other Websites \n\n"""
                markdown_all += generate_html_snippet(news_items, keys, language)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown_all)
            print("Markdown文件已生成: ", output_path) 
        return markdown_all

