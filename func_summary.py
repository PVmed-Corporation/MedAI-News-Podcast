from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
import openai

# 203
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
# 语言模型
def summarize_website_content(url, temperature=1, model_name="gpt-3.5-turbo-16k", chain_type="stuff"):
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

#对话模型
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
