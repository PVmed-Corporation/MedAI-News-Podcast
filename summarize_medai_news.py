from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import WebBaseLoader


messages = [{'role': 'system',
             'content': 'system_message'},
            {'role': 'user',
             'content': 'it should be content or title'}, ]

system_messages = {
    'English': [
        'Summarize the content provided below in a concise manner. Assemble a coherent '
        'script by adeptly consolidating fragmented information and introductions without' 
        'overlooking details. Aim for approximately 100 words and compile a news article'
        'from the given information.',
        'You are a linguist, skilled in summarizing textual content and presenting '
        'it in 3 bullet points using markdown.'
    ],
    'Chinese': [
        
        '你是一位翻译专家。请注意语言流畅、连贯性和中文表达习惯。避免多余或不相关的信息，'
        '专注于将文字翻译成中文。生成的结果需符合新闻格式规范，突出文章核心内容于开篇。',
        '你是个中文杂志编辑， 你说的话将被印在顶级新闻杂志上， 你要检查并删除乱码和无关信息 '
        '生成中文标题，保持内容的一致性直接返回报纸上呈现的标题， 不要返回多余信息，无法翻译的英文保持原文',
        '你是个中文杂志编辑， 你说的话将被印在顶级新闻杂志上， 要检查并删除乱码和无关信息, '
        '生成一段中文总结，保持内容的一致性,不超过250字 '
        '直接返回返回报纸上应该有的报道,不要返回多余信息',
        '你是个中文杂志编辑， 你说的话将被印在顶级新闻杂志上， 要检查并删除乱码和无关信息， '
        '生成三个中文的要点， 保持内容的一致性,不要返回多余信息'
    ],

    'Key':[ '针对以下内容，提炼出2-5个关键词，以简洁方式概括其要点'

    ]
    
}



def LLM_processing_content(llm, client, news_items, language, chain_type="stuff"):
    # Load the summarization chain
    chain = load_summarize_chain(llm, chain_type=chain_type)
    
    # summarize_website_content and translate information to Chinese
    for keys in news_items:
        item = news_items[keys]
        # Load the content from the given URL
        for index, _item in enumerate(item.url_link):
            # if keys not in ["arxiv"]:
            # use Web loader to get info   
            loader = WebBaseLoader(_item)
            docs = loader.load()
                
            # Run the chain on the loaded documents
            web_summarize = chain.run(docs)
            item.get_content(web_summarize)

            if language == 'Chinese': 
                # 提取messsage中内容部分翻译网页信息为中文
                messages[0]['content'] = system_messages['Chinese'][0]
                messages[1]['content'] = item.content[index]

                # TODO --最后输入实际是messages这个列表
                response = client.chat.completions.create(
                                model="gpt-3.5-turbo-16k",
                                messages=messages,
                                temperature=1.0,
                                max_tokens=2048,
                            )
                web_chinese = response.choices[0].message.content

                # # 检查信息正确
                # messages[0]['content'] = system_message[4]
                # messages[1]['content'] = web_chinese

                # response = client.chat.completions.create(
                #                 model="gpt-3.5-turbo-16k",
                #                 messages=messages,
                #                 temperature=1.0,
                #                 max_tokens=2048,
                #             )
                # web_chinese_r = response.choices[0].message.content
                
                # 提取messsage中标题部分翻译网页信息为中文
                messages[0]['content'] = system_messages['Chinese'][1]
                messages[1]['content'] = item.title[index]
                response = client.chat.completions.create(
                                model="gpt-3.5-turbo-16k",
                                messages=messages,
                                temperature=1.0,
                                max_tokens=2048,
                            )
                title_chinese = response.choices[0].message.content

                # # 提取messsage中标题部分翻译网页信息为中文
                # messages[0]['content'] = system_message[3]
                # messages[1]['content'] = title_chinese
                # response = client.chat.completions.create(
                #                 model="gpt-3.5-turbo-16k",
                #                 messages=messages,
                #                 temperature=1.0,
                #                 max_tokens=2048,
                #             )
                # title_chinese_r = response.choices[0].message.content
                
                # add the translation version to collector
                item.get_trans_info(title_chinese, web_chinese)
    
    return


def generate_paper_summary(client, info2summarize, language):
    # 归纳摘要前修改messages中的系统提示为system_message_0
    messages[0]['content'] = system_messages['English'][0]
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
    messages[0]['content'] = system_messages['English'][1]
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
        messages[0]['content'] = system_messages['Chinese'][1]
        messages[1]['content'] = generate_key_points
        
        response = client.chat.completions.create(
                                model="gpt-3.5-turbo-16k",
                                messages=messages,
                                temperature=1.5,
                                max_tokens=4000,
                            )
        generate_key_points = response.choices[0].message.content

        # # 检查信息正确
        # messages[0]['content'] = system_message[5]
        # messages[1]['content'] = generate_key_points

        # response = client.chat.completions.create(
        #                 model="gpt-3.5-turbo-16k",
        #                 messages=messages,
        #                 temperature=1.0,
        #                 max_tokens=2048,
        #             )
        # generate_key_points = response.choices[0].message.content
    
    return generate_key_points

