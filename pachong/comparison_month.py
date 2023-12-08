import matplotlib.pyplot as plt
import pandas as pd

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]

# 读取Excel文件
df = pd.read_excel('旅游景点.xlsx', names=['每日游客数量', '日期'])

# 将日期列转换为日期类型
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 按月份进行分组并计算每月游客总数
monthly_data = df.groupby(df['日期'].dt.to_period("M"))['每日游客数量'].sum().reset_index()

# 创建图形和坐标轴对象
fig, ax1 = plt.subplots(figsize=(10, 7))

# 绘制柱状图
ax1.bar(monthly_data['日期'].dt.strftime('%Y-%m'), monthly_data['每日游客数量'], color='blue', label='每月游客数量')

# 添加标签和标题
ax1.set_xlabel('日期')
ax1.set_ylabel('游客数量', color='blue')
ax1.set_title('每月游客数量对比')

# 旋转日期标签
ax1.set_xticklabels(monthly_data['日期'].dt.strftime('%Y-%m'), rotation=45, ha='right')

# 创建第二个坐标轴对象
ax2 = ax1.twinx()

# 绘制折线图
ax2.plot(monthly_data['日期'].dt.strftime('%Y-%m'), monthly_data['每日游客数量'], color='red', marker='o', label='每月趋势')

# 添加标签和标题
ax2.set_ylabel('趋势', color='red')

# 显示图例
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# 显示图形
plt.savefig("每月游客量对比.jpg")
plt.show()