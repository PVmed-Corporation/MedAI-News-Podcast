import requests
from bs4 import BeautifulSoup

from utils import unify_time, check_date_match


def get_websit_info(url, tag_name, class_name, process_type, local_time, day):
    # 使用requests和beautifulsoup的函数
    # Make a request to a web page, and return the status code
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }

    response = requests.get(url, headers=headers) 
    
    # TODO: delete or not
    web_time = ''

    # Check the status code
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 爬取OPENAI_link
        if process_type == "openai": 
            # 查找具有特定类名的<a>标签
            target_link = soup.find(tag_name, class_=class_name)
            if target_link:
                # 将基本 URL 与相对路径结合
                web_link = url + target_link['href']
                response = requests.get(web_link, headers=headers)
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.content, 'html.parser')
                h1_tag = soup.find("h1", class_="f-display-2")
                if h1_tag:
                    web_titile = h1_tag.text.strip()
                else:
                    print("Couldn't find the <h1> tag with the specified class on the page.")
                    raise ValueError
            else:
                print("Couldn't find the target post URL.")
                raise ValueError  
               
        # 爬取lexfridman_link
        elif process_type == "lexfridman": 
            transcript_link_element = soup.find(tag_name, string="Transcript")
            if transcript_link_element:
                web_link = transcript_link_element['href']
                response = requests.get(web_link, headers=headers)
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.content, 'html.parser')
                h1_tag = soup.find("h1", class_="entry-title")
                if h1_tag:
                    web_titile = h1_tag.text.strip()
                else:
                    print("Couldn't find the <h1> tag with the specified class on the page.")
                    raise ValueError
            else:
                print("Couldn't find the target post URL.")
                raise ValueError   

        # 爬取苹果博客link & title
        elif process_type == "apple": 
            article = soup.select_one(tag_name)
            if article:
                web_link = url + article['href']
                # 根据提供的HTML片段，定位到文章的标题和链接
                web_titile = article.text
            else:
                print("Couldn't find the target post URL.")
                raise ValueError

        # 爬取nvida link & title
        elif process_type == "nvidia":  
            ul_elems = soup.find_all(tag_name)
            all_links = []
            # 从所有 <ul> 元素中提取链接和文本
            for ul_elem in ul_elems:
                links = [(link.get('href'), link.text) for link in ul_elem.find_all('a')]
                all_links.extend(links)
            # 提取指定链接文本对后的第一个链接和文本
            found = False
            for link, text in all_links:
                # print("text1 is", text)
                if found:
                    web_link = link
                    web_titile = text
                    break
                if link == url and text == class_name:
                    found = True
            if not found:
                print("Couldn't find the target post URL.")
                raise ValueError
            
        # 爬取aws link & title
        elif process_type == "aws":  
            articles = soup.find_all(tag_name, class_=class_name)
            if articles:
                web_link = articles[0].find('a')['href']
                web_titile = articles[0].find('h2').text
            else:
                print("Couldn't find the target post URL.")
                raise ValueError
        
        # 爬取microsoft link & title
        elif process_type == "microsoft":  
            # 由于网站可能有多个这样的链接，我们只选择第一个匹配的项
            link_element = soup.find(tag_name, class_=class_name)
            if link_element:
                web_link = link_element['href']
                web_titile = link_element.h3.text.strip()
            else:
                print("Couldn't find the target post URL.")
                raise ValueError

        # 爬取techcrunch link & title
        elif process_type == "techcrunch":  
            # 由于网站可能有多个这样的链接，我们只选择第一个匹配的项
            articles = soup.select('.post-block__title a')
            if articles:
                web_link = articles[0]['href']
                web_titile = articles[0].text
            else:
                print("Couldn't find the target post URL.")
                raise ValueError

        # 爬取机器之心信息
        elif process_type == "机器之心":  
            articles = soup.find(class_=class_name).find("a")
            web_time = soup.find('time', class_='js-time-ago').get_text(strip=True)
            
            # TODO: check the articles and web_time are exist
            web_time = unify_time(web_time)
            
            if check_date_match(web_time, local_time, day) == True:
                if articles:                
                    web_titile = articles.get('alt')
                    web_link = url + articles.get('href')

                else:
                    print("Couldn't find the target post URL.")
                    raise ValueError  
            else:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None
                process_type = None


        # 爬取paper with code信息
        elif process_type == "paperwithcode":  
            articles = soup.find(class_=class_name).find('h1')
            # TODO --0104有报错需要修改位置
            # web_time = soup.find(class_=class_name).find('span', class_='author-name-text item-date-pub').get_text()
            web_time = "20240104"
            # TODO: check the articles and web_time are exist
            web_time = unify_time(web_time)

            if check_date_match(web_time, local_time, day) == True:
                if articles:
                    # 提取 href 值和标题文本
                    web_link = "https://paperswithcode.com" + articles.a['href']
                    web_titile = articles.a.get_text()        
                else:
                    print("Couldn't find the target post URL.")
                    raise ValueError
            else:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None
         
        # auntminnie
        elif process_type == "auntminnie":
            soup = BeautifulSoup(response.content, 'html.parser')   
            a_tag = soup.find(class_=class_name).find(tag_name)
            web_link = url + a_tag.get('href')
            web_titile  = a_tag.get_text()
            
            # 获取时间
            response = requests.get(web_link, headers=headers)
            # response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.content, 'html.parser')
            web_time = soup.find(class_="author-published-node__content-published").get_text()
            web_time = unify_time(web_time)
            if check_date_match(web_time, local_time, day) is not True:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None
        
        # mobi
        elif process_type == "mobihealthnews":
            soup = BeautifulSoup(response.content, 'html.parser')
            web_time = soup.find('div', class_='views-field views-field-created-1').get_text(strip=True)
            web_time = unify_time(web_time)
            
            if check_date_match(web_time, local_time, day) == True:
                a_tag = soup.find(class_=class_name).find(tag_name)
                web_link = url + a_tag.get('href')
                print("mobi web_link here:", web_link)
                web_titile = a_tag.get_text()
                web_time = unify_time(web_time)
            else:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None

        '''
        # TODO: erroe here
        # natureBME
        elif process_type == "natureBME" :
            soup = BeautifulSoup(response.content, 'html.parser') 
            output_test_nature =  str(response.content) 
            web_time = "2024-01-24"
            # web_time = soup.find('div', class_="c-article-header")
            print("natureBME time:", web_time)

            if check_date_match(web_time, local_time, day) == True:
                a_tag = soup.find(class_=class_name).find(tag_name)
                web_link = url + a_tag.get('href')
                a_tag = soup.find(class_=class_name).find(tag_name)
                web_link = a_tag.get('href')
                web_titile = a_tag.get_text()
        
            else:
                print("Time is not valid:", "web_time is: ", web_time, "local_time is: ", local_time)
                url = None
                web_titile = None
                web_link = None
                web_time = None
        '''

        return web_link, web_titile, web_time 

    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        raise ValueError
        

