import pandas as pd


def generate_html_snippet(news_items, keys, language, ):
    markdown_part = ''
    
    for ii, _ in enumerate(news_items[keys].title):
        link = news_items[keys].url_link[ii]
        if language == 'English':
            title = news_items[keys].title[ii]
            content = news_items[keys].content[ii]
            web_time = news_items[keys].web_time[ii]
            publisher = news_items[keys].publisher[ii]
        else:
            title = news_items[keys].trans_title[ii]
            content = news_items[keys].trans_content[ii]
            web_time = news_items[keys].web_time[ii]
            publisher = news_items[keys].publisher[ii]
        
        html_snippet = (
            f"### <a href=\"{link}\" style=\"color: #2859C0; text-decoration: none; "
            f"font-size: 17px; font-weight: bold; font-family: Arial;\"> {title}</a>"
            f"<span style=\"margin-left: 7px; background-color: white; padding: 0px 8px; border: 1px solid rgb(251, 88, 88)"
            f"border-radius: 13px; font-size: 12px; color: rgb(251, 88, 88)\">{publisher}</span>\n\n"
        )
        
        markdown_part += html_snippet
        markdown_part += f"<span style='font-size: 12px; font-family: news-romans;'>{web_time}</span>\n\n"
        markdown_part += f"<span style='font-size: 16px; font-family: news-romans;'>{content}</span>\n\n"
        
    return markdown_part


def generate_dingding_snippet(news_items, keys, language, ):
    markdown_part = ''
    
    for ii, _ in enumerate(news_items[keys].title):
        link = news_items[keys].url_link[ii]
        if language == 'English':
            title = news_items[keys].title[ii]
            content = news_items[keys].content[ii]
            web_time = news_items[keys].web_time[ii]
            publisher = news_items[keys].publisher[ii]

        else:
            title = news_items[keys].trans_title[ii]
            content = news_items[keys].trans_content[ii]
            web_time = news_items[keys].web_time[ii]
            publisher = news_items[keys].publisher[ii]
        
        html_snippet = (
            f"### [{title}   ]({link})"
            f"  {publisher}\n\n"
        )
        
        markdown_part += html_snippet
        markdown_part += f"{web_time}\n\n"
        markdown_part += f"{content}\n\n"
        
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
                        'web_time': news_items[keys].web_time[ii],
                        'URL': news_items[keys].url_link[ii],
                        'Web_Summary': news_items[keys].content[ii]
                    }
                else:
                    entry = {
                        'From': keys,
                        'Eng_Title': news_items[keys].title[ii],
                        'Title': news_items[keys].trans_title[ii],
                        'web_time': news_items[keys].web_time[ii],
                        'URL': news_items[keys].url_link[ii],
                        'publisher': news_items[keys].publisher[ii],
                        'Eng_Web_Summary': news_items[keys].content[ii],
                        'Web_Summary': news_items[keys].trans_content[ii]
                    }                        
                output_list.append(entry)

        # TODO: yichuqu 将列表转换为DataFrame
        df = pd.DataFrame(data=output_list).set_index(["From","Title"])
        with pd.ExcelWriter(output_path) as writer:
            df.to_excel(writer) 
        print("excel文件已生成: ", output_path) 

    elif format == "markdown_dingding":
        # 使用加载的实例
        markdown_all = " "
        markdown_all += """# Med-AI News Podcast\n\n"""
        markdown_all += """## Key Points of Today's News\n\n"""
        markdown_all += LLM_paper_summary + '''\n\n'''

        # 正文的信息排版
        for ii, keys in enumerate(news_items):
            print(keys,"加入md文件")
            if ii<1:
                markdown_all += f"""## Paper from {keys} \n\n"""
            else:
                if ii == 1:
                    markdown_all += """## News from Websites \n\n"""
            markdown_all += generate_dingding_snippet(news_items, keys, language)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown_all)
            print("Markdown文件已生成: ", output_path) 
        return markdown_all

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
            else:
                if ii == 2:
                    markdown_all += """## News from Other Websites \n\n"""
            markdown_all += generate_html_snippet(news_items, keys, language)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown_all)
            print("Markdown文件已生成: ", output_path) 
        return markdown_all

