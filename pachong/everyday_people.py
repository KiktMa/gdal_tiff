import matplotlib.pyplot as plt
import pandas as pd

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]

# 读取Excel文件
df = pd.read_excel('旅游景点.xlsx', names=['每日游客数量', '日期'])

# 将日期列转换为日期类型
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(df['日期'], df['每日游客数量'], marker='o', linestyle='-')
plt.title('每日游客数量趋势')
plt.xlabel('日期')
plt.ylabel('游客数量')
plt.grid(True)
plt.savefig("每日游客数量趋势.jpg")
plt.show()
