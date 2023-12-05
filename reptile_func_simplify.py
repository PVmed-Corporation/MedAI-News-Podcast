import requests
from bs4 import BeautifulSoup
import arxiv

#使用requests和beautifulsoup的函数
def get_info(url, tag_name, class_name, process_type):
    response = requests.get(url)

    if response.status_code == 200: #检测网站状态
        soup = BeautifulSoup(response.content, 'html.parser')

        if process_type == 1: #爬取OPENAI_link
            # 查找具有特定类名的<a>标签
            target_link = soup.find(tag_name, class_=class_name)
            if target_link:
                # Combining base URL with the relative path
                post_url = url + target_link['href']
                return post_url
            else:
                print("Couldn't find the target post URL.")
                return None

        if process_type == 2: #爬取title
            h1_tag = soup.find(tag_name, class_=class_name)
            if h1_tag:
                return h1_tag.text.strip()
            else:
                print("Couldn't find the <h1> tag with the specified class on the page.")
                return None

        if process_type == 3: #爬取lexfridman_link
            transcript_link_element = soup.find('a', string="Transcript")
            if transcript_link_element:
                return transcript_link_element['href']
            else:
                return None

        if process_type == 4: #爬取苹果博客link&title
            article = soup.select_one('h3.post-title a')
            apple_link = 'https://machinelearning.apple.com' + article['href']
            # 根据提供的HTML片段，定位到文章的标题和链接
            Apple_blog_title = article.text
            return  apple_link, Apple_blog_title

        if process_type == 5:  # 爬取nvida link&title
            target_link = "https://blogs.nvidia.com/ai-podcast/"
            target_text = "AI Podcast"
            ul_elems = soup.find_all('ul')
            all_links = []
            # Extract links and texts from all <ul> elements
            for ul_elem in ul_elems:
                links = [(link.get('href'), link.text) for link in ul_elem.find_all('a')]
                all_links.extend(links)
            # Extract the first link and text after the specified link-text pair
            found = False
            for link, text in all_links:
                # print("text1 is", text)
                if found:
                    return link, text
                if link == target_link and text == target_text:
                    found = True

        if process_type == 6:  # 爬取aws link&title
            articles = soup.find_all('div', class_='lb-col lb-mid-18 lb-tiny-24')
            if not articles:
                print("No articles found.")
                return None, None
            title = articles[0].find('h2').text
            link = articles[0].find('a')['href']
            return  link, title

    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None

#使用内置报的函数
def get_arxiv_summary():
    search = arxiv.Search(
        query="AI, LLM, machine learning, NLP",
        #max_results=st.session_state.arxiv,
        max_results=2,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    ariv_essay = ''
    for result in search.results():
        ariv_essay += result.summary
    return ariv_essay