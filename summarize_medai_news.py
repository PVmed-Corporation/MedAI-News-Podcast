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
        'Step 3 - keep the content in 200 words  ".',
        'You are a linguist, skilled in summarizing textual content and presenting '
        'it in 3 bullet points using markdown.',
        'Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness.'
        'Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.'
        'Rely strictly on the provided text, without including external information. Format the summary in one paragraph with in 100 words.',
        'Summarize the news in an objective way, delete newline character, summarizing textual '
        'content in one paragraph, and presenting it in 100 words.'
    ],
    'Chinese': [
        '你是一位新闻翻译专家。请注意语言流畅,连贯性和中文表达习惯。避免多余或不相关的信息,'
        '专注于将文字翻译成中文。生成的结果需符合新闻格式规范,突出文章核心内容于开篇, 用完整的一段话呈现, 控制内容在200字左右。',
        '你是一位新闻翻译专家。请将文字翻译成中文。生成的结果需符合新闻格式规范的中文标题。'
        '请注意语言流畅,连贯性和中文表达习惯, 以及学术名词的使用恰当。避免多余或不相关的信息,',
        '你是个中文杂志编辑, 请将英文翻译成中文,注意中文表达的习惯和简练,生成3个中文的要点, 你说的话将被印在顶级新闻杂志的版面新闻上, 要检查并删除乱码和无关信息, '
        '保持内容的一致性, 不要返回多余信息',
        '你是一位新闻专家。请对下面的文本进行总结,保留核心要点和关键信息,保持信息的准确和凝练,控制字数在200字左右,'
        '接着请将文字翻译成中文。请注意语言流畅,连贯性和中文表达习惯,以及学术名词的使用恰当。避免多余或不相关的信息'
        '最后对结果进行润色,生成的结果需符合新闻格式规范。'
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
    chunk_overlap = 50,
    length_function = len,
)

def gpt_completion_response(client, messages):
    response = client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=messages,
                temperature=1.0,
                max_tokens=4000,
                )
    gpt_output = response.choices[0].message.content

    return gpt_output


def LLM_processing_content(llm, client, news_items, language, chain_type="stuff"):
    # Load the summarization chain
    chain = load_summarize_chain(llm, chain_type=chain_type) # maximum context length is 4097 tokens
    output_test = ''
    output_test += 'chain'  + str(chain)

    # summarize_website_content and translate information to Chinese
    for keys in news_items:
        item = news_items[keys]
        output_test += 'item'  + str(item) + '\n'
        # Load the content from the given URL
        for index, _item in enumerate(item.url_link):
            # gnews special
            if keys not in ["google", "机器之心"]:
                # use Web loader to get info   
                loader = WebBaseLoader(_item)
                docs = loader.load()
                output_test += '【_item】'  + str(_item) + '\n'
                output_test += '【docs】'  + str(docs) + '\n'

                output_test += '【len(str(docs)】'  + str(len(str(docs))) + '\n'
                if len(str(docs)) > 3000:
                    # 当文本总长度超过4000字符时执行拆分
                    chunks = text_splitter_r.split_documents(docs)
                    web_summarize = chain.run(chunks)
                    output_test += '【web_summarize:】'  + str(web_summarize) + '\n'
                
                else:
                    # 当文本总长度不超过4000字符时，不执行拆分，直接处理整个文本
                    web_summarize = chain.run(docs)
                    output_test += '【paper_summarize:】'  + str(web_summarize) + '\n'

                # web_summarize = [chain.run([chunk]) for chunk in text_splitter_c.split_documents(docs)]
                item.get_content(str(web_summarize))

                if language == 'Chinese': 
                    # 提取messsage中内容部分翻译网页信息为中文
                    messages[0]['content'] = system_messages['Chinese'][0]
                    messages[1]['content'] = item.content[index]

                    # TODO --最后输入实际是messages这个列表
                    web_chinese = gpt_completion_response(client, messages)

                    # 提取messsage中标题部分翻译网页信息为中文
                    messages[0]['content'] = system_messages['Chinese'][1]
                    messages[1]['content'] = item.title[index]

                    title_chinese = gpt_completion_response(client, messages)
                    output_test += '【title】'  + str(item.title[index]) + '\n'
                    output_test += '【title_chinese】'  + str(title_chinese) + '\n'
                    output_test += '【web_chinese】'  + str(web_chinese) + '\n'
                    # add the translation version to collector
                    item.get_trans_info(title_chinese, web_chinese)

            # 处理中文的来源
            if keys in ["机器之心"]:
                # 法1--使用gpt模型summarize
                output_test += '【keys】'  + str(keys) + '\n'
                output_test += '【title】'  + str(item.title[index]) + '\n'

                messages[0]['content'] = system_messages['Chinese'][3]
                messages[1]['content'] = item.content[index]
                
                output_test += '【Chinese content (item.content[index])】'  + str(item.content[index]) + '\n'
                
                web_summarize = gpt_completion_response(client, messages).replace("\n", "").replace("/n", "")
                output_test += '【Chinese content (web_summarize1)】'  + str(web_summarize) + '\n'
                
                #  # 扩展列表以确保它至少包含index+1个元素
                # if index >= len(item.content):
                #     item.content.extend([""] * (index + 1 - len(item.content)))

                item.content[index] = str(web_summarize)
                output_test += '【Content after adding item.content】'  + str(item.content) + '\n'

            else:
                # 法1--google 使用gpt模型summarize
                output_test += '【keys】'  + str(keys) + '\n'
                output_test += '【title】'  + str(item.title[index]) + '\n'

                messages[0]['content'] = system_messages['English'][2]
                messages[1]['content'] = item.content[index]      
                output_test += '【google content (item.content[index])】'  + str(item.content[index]) + '\n'
                
                # 得到google新闻的summary
                web_summarize = gpt_completion_response(client, messages)
                web_summarize = web_summarize.replace("\n", "").replace("/n", "")
                output_test += '【google content (web_summarize1)】'  + str(web_summarize) + '\n'

                # print("google web_summarize：", google_summarize)
                # print("item:", item)
                output_test += '【Content before adding item.content】'  + str(item.content) + '\n'
                
                #  # 扩展列表以确保它至少包含index+1个元素
                # if index >= len(item.content):
                #     item.content.extend([""] * (index + 1 - len(item.content)))

                item.content[index] = str(web_summarize)

                output_test += '【Content after adding item.content】'  + str(item.content) + '\n'

                if language == 'Chinese': 
                    # 提取messsage中内容部分翻译网页信息为中文
                    messages[0]['content'] = system_messages['Chinese'][0]
                    messages[1]['content'] = str(web_summarize)

                    web_chinese = gpt_completion_response(client, messages)
                    
                    # 提取messsage中标题部分翻译网页信息为中文
                    messages[0]['content'] = system_messages['Chinese'][1]
                    messages[1]['content'] = item.title[index]

                    title_chinese = gpt_completion_response(client, messages)
                    output_test += '【title】'  + str(item.title[index]) + '\n'
                    output_test += '【title_chinese】'  + str(title_chinese) + '\n'
                    output_test += '【web_chinese】'  + str(web_chinese) + '\n'                    
                    # add the translation version to collector
                    item.get_trans_info(title_chinese, web_chinese)                
     
    with open("output/output.txt", "w") as file:
        # 将字符串写入文件
        file.write(output_test)
    
    return


def generate_paper_summary(client, info2summarize, language):

    # 归纳摘要前修改messages中的系统提示为system_message_0
    messages[0]['content'] = system_messages['English'][0]
    messages[1]['content'] = str(info2summarize)
    
    generate_paper_summary = gpt_completion_response(client, messages)

    # 生成3个key points
    messages[0]['content'] = system_messages['English'][1]
    messages[1]['content'] = generate_paper_summary

    generate_key_points = gpt_completion_response(client, messages)
    
    if language == 'Chinese':
        # 生成key points前修改messages中的系统提示为system_message_2
        messages[0]['content'] = system_messages['Chinese'][2]
        messages[1]['content'] = generate_key_points
        
        generate_key_points = gpt_completion_response(client, messages)
    
    return generate_key_points

