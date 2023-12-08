from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
import openai

'''
# It tries to split on them in order until the chunks
# are small enough. The default list is ["\n\n", "\n", " ", ""].
system_message = '''
                You are a very talented editor, skilled at consolidating 
                fragmented information and introductions into a cohesive script, without missing any details.
                Compile the news article based on the information in 【】.  
                '''

system_message_2 = '''
                You are a linguist, skilled in summarizing textual content and presenting it in 3 bullet points using markdown. 
                '''

system_message_3 = '''
                你是个语言学家，擅长把英文翻译成中文。要注意表达的流畅和使用中文的表达习惯。不要返回多余的信息，只把文字翻译成中文。
                '''
# language model
def summarize(url, temperature=1, model_name="gpt-3.5-turbo-16k", chain_type="stuff"):
# TODO --查函数参数
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

#  generate responses based on the provided context. 
def completion(messages,
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

# mock function
def summarize(url):
    summarized_content = "sum of " + url
    return summarized_content

def completion(content_or_title, a = 'change ', b = 'language ', c = 'style'):
    response = content_or_title + " " + a + b + c
    return response

system_message = ["system_message_1", "system_message_2", "system_message_3"]

# system_message和it should be content or title都是循环中要重新赋值的
messages =  [           {'role':'system',
                        'content': 'system_message'},
                        {'role':'user',
                        'content': 'it should be content or title'},]

# 生成每一个部分的summary
def LLM_processing_content(news_items):
    # summarize_website_content and translate information to Chinese
    for index, item in enumerate(news_items):
        # 归纳网页信息
        web_summarize = summarize(item['url'])
        # 在字典中新增sumarry的内容
        news_items[index]['web_summarize'] = web_summarize

        language = 'chinese' # 这里先设成生成中文了
        if language == 'chinese':
            # TODO --这里还要循环修改message，有点复杂，但是不修改就要每次重新生成一个
            # 提取messsage中内容部分翻译网页信息为中文
            # 中文翻译循环中修改messages中的系统提示为system_message_3
            messages[0]['content'] = system_message[2]
            # 同时修改messages中的内容部分
            messages[1]['content'] = web_summarize
            # 实际上最后输入是messages这个列表, 但是使用前要注意修改messages中的两部分信息
            web_chinese = completion(messages[1]['content']) # TODO --最后输入实际是messages这个列表
            # 新增字典
            # TODO --或许转换成中文不应该同步生成，可能会很慢
            news_items[index]['web_summarize_chinese'] = web_chinese
    
            # TODO --这里中文的部分还要再看看是直接归纳中文信息，还是直接翻译归纳后的
            # 提取messsage中标题部分翻译网页信息为中文
            messages[1]['content'] = news_items[index]['title']
            title_chinese = completion(messages[1]['content'])
            news_items[index]['title_chinese'] = title_chinese
    return news_items

# 生成整个日报的summary
def generate_paper_summary(news_items):

    # 归纳摘要前修改messages中的系统提示为system_message
    messages[0]['content'] = system_message[0]
    # 同时修改messages中的内容部分为全部网页的summary
    summary_whole = [item['web_summarize'] for item in news_items]
    messages[1]['content'] = summary_whole
    generate_paper_summary = completion(str(messages[1]['content'])) # TODO --最后输入实际是messages这个列表
    # test
    language = 'English'
    if language == 'English':
        # 生成key points前修改messages中的系统提示为system_message_2
        messages[0]['content'] = system_message[1]
        # 输入应为上一段整理好的信息
        messages[1]['content'] = generate_paper_summary
        generate_key_points = completion(str(messages[1]['content'])) # TODO --最后输入实际是messages这个列表
    if language == 'Chinese':
        # 生成key points前修改messages中的系统提示为system_message_2
        messages[0]['content'] = system_message[3]
        # 输入应为上一段整理好的信息
        messages[1]['content'] = generate_paper_summary
        generate_key_points = completion(str(messages[1]['content'])) # TODO --最后输入实际是messages这个列表
    return generate_key_points
