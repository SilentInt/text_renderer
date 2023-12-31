import cv2
import random
import os
import shutil
import numpy as np

input_dir = "./ws/output/"
output_dir = "./dataset_sp/images/"  # 图片输出目录
label_dir = "./dataset_sp/labels/"  # 标签输出目录
edges_dir = "./dataset_sp/edges/"  # 边缘输出目录

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)
os.makedirs(label_dir, exist_ok=True)
os.makedirs(edges_dir, exist_ok=True)


def pre_process(image):

    # 将图片转换为HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义黑色的阈值范围
    lower_black = np.array([0, 0, 0])
    # upper_black = np.array([180, 255, 50])
    upper_black = np.array([180, 255, 60])

    # 根据阈值创建掩膜
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # 对掩膜进行闭运算
    # mask = cv2.morphologyEx(
    #    mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    # 对掩模进行膨胀操作
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=5)
    # 进行边缘检测掩模
    # edges = cv2.Canny(image, 100, 200)

    # 定义结构元素（闭运算核）
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # 闭运算
    # closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # 寻找闭合区域
    # contours, hierarchy = cv2.findContours(
    #    closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 填充闭合区域
    # filled = np.zeros_like(mask)
    # cv2.drawContours(filled, contours, -1, 255, thickness=cv2.FILLED)

    # 结合两个掩模
    # result = cv2.bitwise_and(mask, mask, mask=filled)
    # return result
    return mask


def convert_to_yolo():
    parsed_data = None
    parsed_size = None
    with open(input_dir+"labels.json", "r", encoding='utf-8') as file:
        data = eval(file.read())
        parsed_data = data["labels"]
        parsed_size = data["sizes"]

    for img_name, labels in parsed_data.items():
        input_img = input_dir+"images/"+img_name+'.jpg'
        # Open image directory
        img = cv2.imread(input_img)

        # 获取图片尺寸
        image_size = parsed_size[img_name]

        # 黑白边缘掩模处理
        img = pre_process(img)

        # 使用边缘检测函数查找数字的边缘
        edges = cv2.Canny(img, 30, 200)

        # 进行闭运算操作
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # 保存边缘图像
        cv2.imwrite(f"{edges_dir}{img_name}.jpg", edges)

        # 根据边缘图像获取轮廓
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 找到最大的轮廓
        max_contour = max(contours, key=cv2.contourArea)

        # 计算轮廓的边界框
        x, y, w, h = cv2.boundingRect(max_contour)

        # 计算数字的中心坐标、宽度和高度
        center_x = x + w // 2
        center_y = y + h // 2
        width = w
        height = h

        # 归一化坐标
        center_x_norm = center_x / image_size[0]
        center_y_norm = center_y / image_size[1]
        width_norm = width / image_size[0]
        height_norm = height / image_size[1]

        # 保存标签
        label = f"{labels} {center_x_norm} {center_y_norm} {width_norm} {height_norm}"

        # 保存图片
        cv2.imwrite(f"{output_dir}{img_name}.jpg", img)
        # shutil.copy(f"{edges_dir}{img_name}.jpg", output_dir)

        # 保存标签到txt文件
        with open(f"{label_dir}{img_name}.txt", "w") as file:
            file.write(f"{label}\n")


convert_to_yolo()
shutil.copy('./classes.txt', label_dir)


# 设置原始数据集路径和目标路径
dataset_path = "dataset_sp"
train_images_path = "datasets/images/train"
train_labels_path = "datasets/labels/train"

val_images_path = "datasets/images/val"
val_labels_path = "datasets/labels/val"
test_images_path = "datasets/test_images"

# 创建目标文件夹
os.makedirs(train_images_path, exist_ok=True)
os.makedirs(val_images_path, exist_ok=True)
os.makedirs(train_labels_path, exist_ok=True)
os.makedirs(val_labels_path, exist_ok=True)
os.makedirs(test_images_path, exist_ok=True)

# 获取原始图像文件列表
images_folder = os.path.join(dataset_path, "images")
image_files = [f for f in os.listdir(
    images_folder) if os.path.isfile(os.path.join(images_folder, f))]

# 随机打乱图像文件列表
random.shuffle(image_files)

# 确定测试集的图像数量（这里假设使用10%的图像作为测试集）
num_test_images = int(0.1 * len(image_files))

# 打印图像数量
print("Total images: ", len(image_files))

print("Num test images: ", num_test_images)
print("Num train images: ", len(image_files) - num_test_images)

# 复制测试集的图像到测试集的文件夹中
for i in range(num_test_images):
    image_file = image_files[i]
    image_src = os.path.join(images_folder, image_file)
    image_dst = os.path.join(val_images_path, image_file)
    shutil.copy(image_src, image_dst)

    # 对应的标签文件
    label_file = image_file.replace(".jpg", ".txt")
    label_src = os.path.join(dataset_path, "labels", label_file)
    label_dst = os.path.join(val_labels_path, label_file)
    shutil.copy(label_src, label_dst)

# 复制剩余的图像到训练集的文件夹中
for i in range(num_test_images, len(image_files)):
    image_file = image_files[i]
    image_src = os.path.join(images_folder, image_file)
    image_dst = os.path.join(train_images_path, image_file)
    shutil.copy(image_src, image_dst)

    # 对应的标签文件
    label_file = image_file.replace(".jpg", ".txt")
    label_src = os.path.join(dataset_path, "labels", label_file)
    label_dst = os.path.join(train_labels_path, label_file)
    shutil.copy(label_src, label_dst)
