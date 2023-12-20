# 使用pandas输出内容
# 循环添加条目到列表中
import pandas as pd
def generate_df_summary(news_items, language):
    output_list = []
    for keys in news_items:
        for ii, _ in enumerate(news_items[keys].title):
            if language == 'English':
                entry = {
                    'From': keys,
                    'Title': news_items[keys].title[ii],
                    'URL': news_items[keys].url_link[ii],
                    'Web_Summary': news_items[keys].content[ii]
                }
            else:
                entry = {
                    'From': keys,
                    'Title': news_items[keys].trans_title[ii],
                    'URL': news_items[keys].url_link[ii],
                    'Web_Summary': news_items[keys].trans_content[ii]
                }                        
            output_list.append(entry)

    # 将列表转换为DataFrame
    df = pd.DataFrame(data=output_list).set_index(["From","Title"])
    with pd.ExcelWriter("web_sum_output.xlsx") as writer:
        df.to_excel(writer) 
    print(df)
    return
