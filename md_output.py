import markdown
import pickle
from medai_news_podcast_api import Source
markdown_text1 = """

# 标题

这是一个示例Markdown文档，包含一些 *斜体* 和 **粗体** 文本。
1220 paper summary

"""

markdown_text2 = """

## 列表

- 项目一
- 项目二
- 项目三

## 代码块

```python
print("Hello, Markdown!")
"""
# 从文件中加载实例


with open('source_instance.pkl', 'rb') as f:
    news_items = pickle.load(f)

# 使用加载的实例
# print("loaded_instance.name", loaded_instance.name)  # 输出: Example
print(type(news_items))
for keys in news_items:
    print("info from:", keys)
    for ii, _ in enumerate(news_items[keys].title):
        print(ii)
        print("url:", news_items[keys].url_link[ii])
        print("title:", news_items[keys].title[ii])
        print("web_summarize:", news_items[keys].content[ii])

markdown_all = markdown_text1 + markdown_text2

with open('md_output.md', 'w', encoding='utf-8') as file:
    file.write(markdown_all)

print("Markdown文件已生成：md_output.md")