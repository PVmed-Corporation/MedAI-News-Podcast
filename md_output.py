import markdown
import pickle
from medai_news_podcast_api import Source

# 从文件中加载实例
with open('source_instance_cn.pkl', 'rb') as f:
    news_items = pickle.load(f)

def generate_md_summary(news_items, language):
    # 使用加载的实例
    markdown_all = ""

    for keys in news_items:
        print({keys})
        markdown_all += f"## Info from: {keys}\n"
        for ii, _ in enumerate(news_items[keys].title):
            if language == 'English':
                markdown_all += f"  - **URL:** {news_items[keys].url_link[ii]}\n"
                markdown_all += f"- **Title:** {news_items[keys].title[ii]}\n"
                markdown_all += f"  - **Web Summary:** {news_items[keys].content[ii]}\n\n"
                
            # TODO -- 待整理
            else:
                markdown_all += f"  - **URL:** {news_items[keys].url_link[ii]}\n"
                markdown_all += f"- **Title:** {news_items[keys].trans_title[ii]}\n"
                markdown_all += f"  - **Web Summary:** {news_items[keys].trans_content[ii]}\n\n"
    with open('md_output.md', 'w', encoding='utf-8') as file:
        file.write(markdown_all)
    print("Markdown文件已生成：md_output.md")

    return

generate_md_summary(news_items, 'English')