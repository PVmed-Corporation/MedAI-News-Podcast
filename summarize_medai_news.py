from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
import openai
# TODO --在可以使用openai模型后可以删掉注释，以及后面的同名函数，并在调用函数时直接输入messages部分
'''
system_message = ('You are a very talented editor, skilled at consolidatingfragmented'
                  ' information and introductions into a cohesive script, without missing'
                  ' any details. Compile the news article based on the information in 【】. ')

system_message_2 = ('You are a linguist, skilled in summarizing textual content and presenting'
                    ' it in 3 bullet points using markdown. ')

system_message_3 = ('你是个语言学家，擅长把英文翻译成中文。要注意表达的流畅和使用中文的表达习惯。'
                    '不要返回多余的信息，只把文字翻译成中文。')

# 语言模型
def summarize_website_content(url, temperature=1, model_name="gpt-3.5-turbo-16k", chain_type="stuff"):
    if True:
        # Load the content from the given URL
        loader = WebBaseLoader(url)
        docs = loader.load()
        # Initialize the ChatOpenAI model
        llm = ChatOpenAI(temperature=temperature, model_name=model_name)
        # Load the summarization chain
        chain = load_summarize_chain(llm, chain_type=chain_type)
        # Run the chain on the loaded documents
        summarized_content = chain.run(docs)
        return summarized_content
    else:
        return 'No result'

# 对话模型
#  generate responses based on the provided context. 可以输入sys，human，ai
def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo-16k",
                                 temperature=1.5, max_tokens=7000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]
'''

# TODO --模拟函数可以跑通
def summarize(url):
    summarized_content = "sum of " + url
    return summarized_content

def completion(content_or_title, a = 'change ', b = 'language ', c = 'style'):
    response = content_or_title + " " + a + b + c
    return response

system_message = ["system_message_1: cohesive", "system_message_2: 3 points", "system_message_3: translate"]

# TODO --system_message和it should be content or title都是循环中要重新赋值的
messages =  [           {'role':'system',
                        'content': 'system_message'},
                        {'role':'user',
                        'content': 'it should be content or title'},]
def LLM_processing_content(news_items, language):
    # summarize_website_content and translate information to Chinese
    for index, item in enumerate(news_items):
        # 调用summarize函数归纳网页信息
        web_summarize = summarize(item['url'])
        news_items[index]['web_summarize'] = web_summarize

        if language == 'English':
            # 处理英文情况的逻辑
            pass

        elif language == 'Chinese':
            # 提取messsage中内容部分翻译网页信息为中文
            # 中文翻译循环中修改messages中的系统提示为system_message_3
            messages[0]['content'] = system_message[2]
            # 同时修改messages中的内容部分
            messages[1]['content'] = web_summarize
            web_chinese = completion(messages[1]['content'])   # TODO --最后输入实际是messages这个列表
            news_items[index]['web_summarize_chinese'] = web_chinese
            # 提取messsage中标题部分翻译网页信息为中文
            messages[1]['content'] = news_items[index]['title']
            title_chinese = completion(messages[1]['content'])
            news_items[index]['title_chinese'] = title_chinese

    return news_items
def generate_paper_summary(news_items, language):
    # 归纳摘要前修改messages中的系统提示为system_message
    messages[0]['content'] = system_message[0]
    # 同时修改messages中的内容部分为全部网页的summary
    summary_whole = [item['web_summarize'] for item in news_items]
    messages[1]['content'] = summary_whole
    generate_paper_summary = completion(str(messages[1]['content'])) # TODO --最后输入实际是messages这个列表

    if language == 'English':
        # 生成key points前修改messages中的系统提示为system_message_2
        messages[0]['content'] = system_message[1]
        # 输入应为上一段整理好的信息
        messages[1]['content'] = generate_paper_summary
        generate_key_points = completion(str(messages[1]['content'])) # TODO --最后输入实际是messages这个列表
    elif language == 'Chinese':
        # 生成key points前修改messages中的系统提示为system_message_2
        messages[0]['content'] = system_message[2]
        # 输入应为上一段整理好的信息
        messages[1]['content'] = generate_paper_summary
        generate_key_points = completion(str(messages[1]['content'])) # TODO --最后输入实际是messages这个列表
    return generate_key_points

# 收集并直接生成arxiv的summary
import arxiv
arxiv_items = [ ]
def get_arxiv_summary(language, max_results ):
    search = arxiv.Search(
        query="AI, LLM, machine learning, NLP",
        # max_results=st.session_state.arxiv,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    for index, result in enumerate(search.results()):
        new_paper = {'paper from': "arxiv", 'paper_summary': result.summary, 'paper_title': result.title}
        arxiv_items.append(new_paper)
        if language == 'English':
            pass
        elif language == 'Chinese':
            new_paper_summary_Chinese = completion(new_paper['paper_summary'])
            new_paper_title_Chinese = completion(new_paper['paper_title']) # 这里需要用system_message_3
            # 新增字典
            arxiv_items[index]['paper_summarize_Chinese'] = new_paper_summary_Chinese
            arxiv_items[index]['paper_title_Chinese'] = new_paper_title_Chinese
    return arxiv_items
