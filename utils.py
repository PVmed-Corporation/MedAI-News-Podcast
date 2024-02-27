import re
import requests
import pypdf
from io import BytesIO
from dateutil import parser
from datetime import datetime, timedelta


def unify_time(input_time):
    # 时间处理函数
    parsed_date = parser.parse(input_time)
    web_time = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    return web_time


def check_date_match(paper_time, current_time, day):
    if isinstance(paper_time, datetime):
        paper_time = paper_time.strftime("%Y-%m-%d %H:%M:%S")
    
    paper_date = paper_time[:10]

    if day == "today":
        # 提取当天
        juedge_time = current_time[:10]
    
    else:
        # 提取前一天
        current_time_ = datetime.strptime(current_time, '%Y-%m-%d-%H-%M-%S')
        juedge_time = str(current_time_ - timedelta(days=1))
        juedge_time = juedge_time[:10]

    # [:10检查日期部分是否一致
    if paper_date == juedge_time:
        return True
    else:
        return False
    

def strtime2date(current_time, day):
    current_time = datetime.strptime(current_time, '%Y-%m-%d-%H-%M-%S')
    yesterday = current_time - timedelta(days=1)
    before_yesterday = current_time - timedelta(days=2)
    if day == "today":
        day = (current_time.year, current_time.month, current_time.day)
        day_before = (yesterday.year, yesterday.month, yesterday.day)
    elif day == "yesterday":
        # 提取前一天
        day = (yesterday.year, yesterday.month, yesterday.day)
        day_before = (before_yesterday.year, before_yesterday.month, before_yesterday.day)
    else:
        raise ValueError("The value of day is wrong")
        
    return day, day_before


def extract_text_from_pdf(url):
    # 从 URL 下载 PDF 文件内容，读取pdf第一页文本
    response = requests.get(url)
    response.raise_for_status()

    # 使用 BytesIO 读取下载的 PDF 内容
    with BytesIO(response.content) as open_pdf_file:
        # 读取 PDF 文件
        pdf_reader = pypdf.PdfReader(open_pdf_file)
        
        # 获取第一页的文本
        first_page = pdf_reader.pages[0]
        text = first_page.extract_text()
    
    return text


def find_educational_institutions(text):
    # TODO -- 还需要优化pattern
    # 通过前后文本匹配
    # 匹配机构名称，并返回第一个匹配到的机构名前后100个字符的文本字符串
    pattern = r'([A-Z][^\s,.]+[.]?\s[(]?)*(College|University|Institute|School|School of|Academy)[^,\d]*(?=,|\d)'
    # match = re.search(pattern, text)  # 使用 re.search() 查找第一个匹配项
    match = re.finditer(pattern, text)
    match_list = [i.span() for i in match]
    if len(match_list) > 0:
        start_pos = max(0, match_list[0][0] - 100)  # 防止索引为负
        end_pos = match_list[-1][-1] + 50 
        institution_text = text[start_pos:end_pos]
        institution_text = institution_text.replace('\n', '') 
        return institution_text  # 返回匹配到的机构名前100后200个字符的文本字符串
    return None  


def select_news_items(list_A, list_B):

    # 按照目标列表A（config_google_publisher）的顺序和范围筛选列表B（gnews获取到的list）
    list_A = [a.lower() for a in list_A]
    list_B = [{**b, 'publisher': {**b['publisher'], 'title': b['publisher']['title'].lower()}} for b in list_B]

    selected_items = []
    other_items = []
    selected_idx = []
    for _idx, _publi in enumerate(list_A):
        for gn_dict in list_B:
            if gn_dict['publisher']['title'] == _publi:
                selected_items.append(gn_dict)
                selected_idx.append(_idx)
            else:
                other_items.append(gn_dict)
        
    # sort the selected papers
    if len(selected_items) > 0:
        sorted_lists = sorted(zip(selected_idx, selected_items))
        selected_idx, selected_items = zip(*sorted_lists)    
    else:
        print("gnews get nothing, you may want to check it now!")

    # get the print gnews
    selected_items = list(selected_items)
    if len(selected_items) >= 3:
        selected_items = selected_items[:3]
    else:
        backup_num = 3-len(selected_items)
        selected_items.extend(other_items[:backup_num])
    
    return selected_items

