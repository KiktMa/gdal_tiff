import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]

data = {
    "accumulo": [249, 777, 1358, 12818, 56015, 105945, 206843],
    "hbase": [3749, 20318, 47155, 299967, 1209378, 1963400, 4682559],
    "mysql": [37, 164, 5090, 30356, 278479, None, None],  # Replace None with actual values if available
}

point_cloud_sizes = [10000, 50000, 100000, 1000000, 5000000, 10000000, 23000000]

plt.figure(figsize=(10, 6))
plt.plot(point_cloud_sizes, data["accumulo"], marker='o', label="Accumulo")
plt.plot(point_cloud_sizes, data["hbase"], marker='o', label="HBase")
plt.plot(point_cloud_sizes, data["mysql"], marker='o', label="MySQL")

plt.xscale("log")  # Use logarithmic scale for x-axis
plt.yscale("log")  # Use logarithmic scale for y-axis
plt.xlabel("点云数据量")
plt.ylabel("读取耗时(ms)")
plt.title("不同存储模型点云查询时间对比")
plt.legend()
plt.grid(True)
plt.savefig("query_time_vs_point_cloud.png")
plt.show()