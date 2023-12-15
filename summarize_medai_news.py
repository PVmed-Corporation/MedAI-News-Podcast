from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import WebBaseLoader


messages = [{'role': 'system',
             'content': 'system_message'},
            {'role': 'user',
             'content': 'it should be content or title'}, ]

system_message = ['You are a very talented editor, skilled at consolidatingfragmented'
                  'information and introductions into a cohesive script, without missing'
                  'any details. Compile the news article based on the information given ',
                  'You are a linguist, skilled in summarizing textual content and presenting'
                  ' it in 3 bullet points using markdown. ',
                  '你是个语言学家，擅长把英文翻译成中文。要注意表达的流畅和使用中文的表达习惯。'
                  '不要返回多余的信息，只把文字翻译成中文。']


def LLM_processing_content(llm, client, news_items, language, chain_type="stuff"):
    # Load the summarization chain
    chain = load_summarize_chain(llm, chain_type=chain_type)
    
    # summarize_website_content and translate information to Chinese
    for keys in news_items:
        item = news_items[keys]
        # Load the content from the given URL
        for index, _item in enumerate(item.url_link):
            if keys not in ["arxiv"]:
                # use Web loader to get info   
                loader = WebBaseLoader(_item)
                docs = loader.load()
                
                # Run the chain on the loaded documents
                web_summarize = chain.run(docs)
                item.get_content(web_summarize)

            if language == 'Chinese': 
                # 提取messsage中内容部分翻译网页信息为中文
                messages[0]['content'] = system_message[2]
                messages[1]['content'] = item.content[index]

                # TODO --最后输入实际是messages这个列表
                response = client.chat.completions.create(
                                model="gpt-3.5-turbo-16k",
                                messages=messages,
                                temperature=1.5,
                                max_tokens=2048,
                            )
                web_chinese = response.choices[0].message.content

                # 提取messsage中标题部分翻译网页信息为中文
                messages[1]['content'] = item.title[index]
                response = client.chat.completions.create(
                                model="gpt-3.5-turbo-16k",
                                messages=messages,
                                temperature=1.5,
                                max_tokens=2048,
                            )
                title_chinese = response.choices[0].message.content
                
                # add the translation version to collector
                item.get_trans_info(title_chinese, web_chinese)
    
    return


def generate_paper_summary(client, info2summarize, language):
    # 归纳摘要前修改messages中的系统提示为system_message_0
    messages[0]['content'] = system_message[0]
    messages[1]['content'] = str(info2summarize)
    
    response = client.chat.completions.create(
                                model="gpt-3.5-turbo-16k",
                                messages=messages,
                                temperature=1.5,
                                max_tokens=4000,
                            )
    generate_paper_summary = response.choices[0].message.content

    # 生成3个key points
    # 生成key points前修改messages中的系统提示为system_message_1
    # 输入应为上一段整理好的信息
    messages[0]['content'] = system_message[1]
    messages[1]['content'] = generate_paper_summary

    response = client.chat.completions.create(
                                model="gpt-3.5-turbo-16k",
                                messages=messages,
                                temperature=1.5,
                                max_tokens=4000,
                            )
    generate_key_points = response.choices[0].message.content
    
    if language == 'Chinese':
        # 生成key points前修改messages中的系统提示为system_message_2
        messages[0]['content'] = system_message[2]
        messages[1]['content'] = generate_key_points
        
        response = client.chat.completions.create(
                                model="gpt-3.5-turbo-16k",
                                messages=messages,
                                temperature=1.5,
                                max_tokens=4000,
                            )
        generate_key_points = response.choices[0].message.content
    
    return generate_key_points

