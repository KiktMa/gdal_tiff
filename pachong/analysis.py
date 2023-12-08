import pandas as pd

# 读取Excel文件，假设有两列分别为"日期"和"数字"
df = pd.read_excel('旅游景点.xlsx', names=['数字', '日期'])

# 将日期列转换为日期类型
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 按月份进行分组并累加数字
result = df.groupby(df['日期'].dt.to_period("M"))['数字'].sum().reset_index()

# 保存结果到新的Excel文件
result.to_excel('每月游客统计.xlsx', index=False)
