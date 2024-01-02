from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter


messages = [{'role': 'system',
             'content': 'system_message'},
            {'role': 'user',
             'content': 'it should be content or title'}, ]


system_messages = {
    'English': [
        'Use the following step-by-step instructions to respond to user inputs.'
        'Step 1 - The user will provide you with text in triple quotes. Summarize'
        'the content in a concise manner in one paragraph. Assemble a coherent script by adeptly' 
        'consolidating fragmented information and introductions without' 
        'overlooking details. '
        'Step 2 - Summarize this text in one sentence and add it to the front of this paragraph.'
        'Step 3 - Embellish it with news language  ".',
        'You are a linguist, skilled in summarizing textual content and presenting '
        'it in 3 bullet points using markdown.',
        'Summarize the news in an objective way, you are skilled in summarizing textual '
        'content in one paragraph, and presenting it in 100 words.'
    ],
    'Chinese': [
        '你是一位新闻翻译专家。请注意语言流畅、连贯性和中文表达习惯。避免多余或不相关的信息，'
        '专注于将文字翻译成中文。生成的结果需符合新闻格式规范，突出文章核心内容于开篇, 用完整的一段话呈现, 控制内容在200字左右。',
        '你是一位新闻翻译专家。请将文字翻译成中文。生成的结果需符合新闻格式规范的中文标题。'
        '请注意语言流畅、连贯性和中文表达习惯，以及学术名词的使用恰当。避免多余或不相关的信息，',
        '你是个中文杂志编辑, 请将英文翻译成中文，注意中文表达的习惯和简练，生成3个中文的要点, 你说的话将被印在顶级新闻杂志的版面新闻上, 要检查并删除乱码和无关信息, '
        '保持内容的一致性, 不要返回多余信息',
        '你是一位新闻专家。请对下面的文本进行总结，保留核心要点和关键信息，保持信息的准确和凝练，控制字数在200字左右，'
        '接着请将文字翻译成中文。请注意语言流畅、连贯性和中文表达习惯，以及学术名词的使用恰当。避免多余或不相关的信息'
        '最后对结果进行润色，生成的结果需符合新闻格式规范。',
    ],

    'Key':[ '针对以下内容, 提炼出2-5个关键词, 以简洁方式概括其要点'

    ]
    
}

# 法一：按特殊字节分割的文档分割器，可能连贯性更好，但对网页这样乱码较多的内容不太适用
text_splitter_c = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1500,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)
# 法二：按字符数量的文档分割器，可能连贯性差一点，但是对网页和text这样多种形式的文本的普适性好
text_splitter_r = RecursiveCharacterTextSplitter(
    chunk_size = 3000,
    chunk_overlap = 20,
    length_function = len,
)

def LLM_processing_content(llm, client, news_items, language, chain_type="stuff"):
    # Load the summarization chain
    chain = load_summarize_chain(llm, chain_type=chain_type) # maximum context length is 4097 tokens
    
    # summarize_website_content and translate information to Chinese
    for keys in news_items:
        item = news_items[keys]
        # Load the content from the given URL
        for index, _item in enumerate(item.url_link):
            # gnews special
            if keys not in ["google"]:
                # use Web loader to get info   
                loader = WebBaseLoader(_item)
                docs = loader.load()
                print("keys:", keys, '\n', 'docs:', docs, '\n\n')
                print(len(str(docs)))
                if len(str(docs)) > 3000:
                    # 当文本总长度超过4000字符时执行拆分
                    chunks = text_splitter_r.split_documents(docs)
                    web_summarize = chain.run(chunks)
                    # web_summarize = [chain.run([chunk]) for chunk in chunks]
                else:
                    # 当文本总长度不超过4000字符时，不执行拆分，直接处理整个文本
                    web_summarize = chain.run(docs)
                
                # summaries = []
                # for chunk in chunks:
                #     summary = chain.run([chunk])
                #     summaries.append(summary)

                # web_summarize = [chain.run([chunk]) for chunk in text_splitter_c.split_documents(docs)]
                item.get_content(str(web_summarize))

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
                    
                    # add the translation version to collector
                    item.get_trans_info(title_chinese, web_chinese)

            else:
                if language == 'Chinese': 

                    # # 法1--使用gpt模型summarize
                    # messages[0]['content'] = system_messages['English'][2]
                    # messages[1]['content'] = item.content[index]

                    # # TODO --最后输入实际是messages这个列表
                    # response = client.chat.completions.create(
                    #                 model="gpt-3.5-turbo-16k",
                    #                 messages=messages,
                    #                 temperature=1.0,
                    #                 max_tokens=2048,
                    #             )
                    # web_chinese = response.choices[0].message.content

                    # 法2--使用longchian summarize
                    docs = item.content[index]
                    if len(str(docs)) > 3000:
                        chunks = text_splitter_r.split_text(docs)            
                        chunks = text_splitter_r.create_documents(chunks) 
                        paper_summarize = chain.run(chunks)
                        # paper_summarize = [chain.run([chunk]) for chunk in chunks]
                    else:
                    # 当文本总长度不超过4000字符时，不执行拆分，直接处理整个文本
                        docs = text_splitter_r.create_documents(docs)
                        # print("docs", docs)
                        paper_summarize = chain.run(docs)

                    # summaries = []
                    # for chunk in chunks:
                    #     print("chunk", chunk)
                    #     summary = chain.run([chunk])
                    #     summaries.append(summary) 
                                             
                    # print("docs:", docs, "\n", "summaries:", summaries, "\n")
                    item.get_content(str(paper_summarize))

                    # 提取messsage中内容部分翻译网页信息为中文
                    messages[0]['content'] = system_messages['Chinese'][0]
                    messages[1]['content'] = str(paper_summarize)

                    # TODO --最后输入实际是messages这个列表
                    response = client.chat.completions.create(
                                    model="gpt-3.5-turbo-16k",
                                    messages=messages,
                                    temperature=1.0,
                                    max_tokens=2048,
                                )
                    web_chinese = response.choices[0].message.content

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
        messages[0]['content'] = system_messages['Chinese'][2]
        messages[1]['content'] = generate_key_points
        
        response = client.chat.completions.create(
                                model="gpt-3.5-turbo-16k",
                                messages=messages,
                                temperature=1.5,
                                max_tokens=4000,
                            )
        generate_key_points = response.choices[0].message.content

    
    return generate_key_points

