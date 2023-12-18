# 使用pandas输出内容
import pandas as pd
def dataframe_output(news_items, language='English'):
# 创建空的 DataFrame
    df = pd.DataFrame(columns=['Title', 'URL', 'Web_Summary'])

    for keys in news_items:
        print(keys)
        '''
        for ii, _ in enumerate(news_items[keys].title):
            title = news_items[keys].title[ii]
            url = news_items[keys].url_link[ii]
            
            if language == 'English':
                web_summary = news_items[keys].content[ii]
            else:
                web_summary = news_items[keys].trans_content[ii]

            # 将新的一行添加到 DataFrame
            df = df.append({'Title': title, 'URL': url, 'Web_Summary': web_summary}, ignore_index=True)
            print(df)
        '''
    return df
