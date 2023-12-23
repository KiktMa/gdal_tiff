from PIL import Image

# 输入和输出文件路径
input_tiff_path = r"C:\Users\mj\Documents\WeChat Files\wxid_daf8d34bzqvz22\FileStorage\File\2023-12\merge(1)(1)\merge\new.tif"
output_jpeg_path = r"C:\Users\mj\Documents\WeChat Files\wxid_daf8d34bzqvz22\FileStorage\File\2023-12\merge(1)(1)\merge\new.jpeg"

# 打开TIFF文件并保存为JPEG
img = Image.open(input_tiff_path)
img.convert('RGB').save(output_jpeg_path, 'JPEG', quality=100)