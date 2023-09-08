from PIL import Image

# 打开图片
image = Image.open("C:\\Users\\mj\\Desktop\\微信图片_20230908162808.jpg")  # 替换为你的图片文件路径

# 将图片转换为RGB模式（如果不是）
image = image.convert('RGB')

# 获取图片的宽度和高度
width, height = image.size

# 定义要替换的粉色范围（根据你的需求调整）
pink_lower = (221, 140, 186)  # 最小粉色RGB值
pink_upper = (246, 196, 223)  # 最大粉色RGB值

# 定义要替换成的蓝色RGB值（根据你的需求调整）
blue_color = (0, 162, 232)

# 创建一个新的图片对象，用于存储替换后的图片
new_image = Image.new('RGB', (width, height))

# 遍历图片的每个像素
for x in range(width):
    for y in range(height):
        pixel = image.getpixel((x, y))
        if pink_lower <= pixel <= pink_upper:
            new_image.putpixel((x, y), blue_color)
        else:
            new_image.putpixel((x, y), pixel)

# 保存替换后的图片
new_image.save("C:\\Users\\mj\\Desktop\\blue.jpg")  # 替换为你想保存的文件路径


