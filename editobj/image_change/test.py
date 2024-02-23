import cv2
import numpy as np

# 读取图像
image = cv2.imread(r"C:\Users\mj\Code\Obj\merge\01581052_2.jpg")

# 获取图像的宽度和高度
height, width, _ = image.shape

# 定义逆时针方向的倾斜角度
angle = 20

# 计算逆时针方向的倾斜矩阵
matrix = np.float32([[1, np.tan(np.radians(angle)), 0],
                    [0, 1, 0]])

# 应用仿射变换
skewed_image = cv2.warpAffine(image, matrix, (width, height), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
cv2.imwrite('skewed_image.jpg', skewed_image)
# 显示原始和倾斜后的图像
# cv2.imshow('Original Image', image)
# cv2.imshow('Skewed Image', skewed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
