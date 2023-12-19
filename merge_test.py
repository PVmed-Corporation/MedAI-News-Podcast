import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas import ExcelWriter
'''
# 创建一个包含重复值的DataFrame对象
data = {'Name': ['John', 'John', 'Alice', 'Bob', 'Bob'],
        'Age': [25, 25, 28, 30, 30],
        'City': ['New York', 'New York', 'Los Angeles', 'Chicago', 'Chicago']}
df = pd.DataFrame(data)
print("data:", data)

# 创建一个新的Excel文件
wb = Workbook()
ws = wb.active

# 将DataFrame对象中的数据写入到Excel文件中
for row in dataframe_to_rows(df, index=False, header=True):
    ws.append(row)

# 合并相同内容的单元格
for column in ws.columns:
    values = [cell.value for cell in column]
    print ("values:", values)
    for i in range(1, len(values)):  
        print(values[i])      
        if values[i] == values[i - 1]:            
            ws.merge_cells(start_row=i + 1, start_column=column[0].column, end_row=i + 2, end_column=column[0].column)

# 保存Excel文件
wb.save('merged_cells.xlsx')
'''
# 创建一个包含重复值的DataFrame对象
data = {'Name': ['John', 'John', 'Alice', 'Bob', 'Bob'],
        'Age': [25, 25, 28, 30, 30],
        'City': ['New York', 'New York', 'Los Angeles', 'Chicago', 'Chicago']}

data = pd.DataFrame(data)
df = pd.DataFrame(data=data).set_index(["Name","Age"])
print(df)
with pd.ExcelWriter("test_output.xlsx") as writer:
    df.to_excel(writer) 

'''
with pd.ExcelWriter(path="excel_file.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(excel_writer=writer, sheet_name="Inventories")
    old_ws = writer.sheets.get("Inventories")
    for col, val in enumerate(df.reset_index().columns):
        old_ws.write(0, col, val)
'''