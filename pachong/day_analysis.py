import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]

# 读取Excel文件
df = pd.read_excel('旅游景点.xlsx', names=['游客人数', '日期'], header=None)

# 将日期列转换为日期类型
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 排序数据按照日期
df = df.sort_values(by='日期')

# 绘制柱状图和折线图
fig, ax1 = plt.subplots()

# 绘制柱状图
ax1.bar(df['日期'], df['游客人数'], color='b', alpha=0.7, label='游客人数')

# 创建第二个y轴用于绘制折线图
ax2 = ax1.twinx()
ax2.plot(df['日期'], df['游客人数'], color='r', label='游客人数折线')

# 设置图例
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# 设置x轴标签旋转
plt.xticks(rotation=45)

# 设置图表标题和轴标签
plt.title('2020年10月到2023年11月每日旅游人数可视化')
ax1.set_xlabel('日期')
ax1.set_ylabel('游客人数', color='b')
ax2.set_ylabel('游客人数折线', color='r')

# 显示图表
plt.savefig("每日旅游人数可视化.jpg")
plt.show()
