import random
import os
import shutil
import cv2

input_dir = "./ws/output/"
dataset_path = './datasets/'


def process_img(img):
    # 形态学膨胀运算
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)
    # 高斯模糊
    img = cv2.GaussianBlur(img, (7, 7), 2)

    # 转化二值图像为灰度图
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # # 自适应阈值二值化
    # img = cv2.adaptiveThreshold(
    #     img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 2)
    # 图像二值化
    ret, img = cv2.threshold(
        img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # 转化为3通道图像
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # 将该图像填充为长:宽=5:3
    height, width = img.shape[:2]
    if height / width < 5/3:
        # 高度不足，上下填充
        top = (width * 5 // 3 - height) // 2
        bottom = width * 5 // 3 - height - top
        img = cv2.copyMakeBorder(img, top, bottom, 0, 0,
                                 cv2.BORDER_CONSTANT, value=[0, 0, 0])
    elif height / width > 5/3:
        # 宽度不足，左右填充
        left = (height * 3 // 5 - width) // 2
        right = height * 3 // 5 - width - left
        img = cv2.copyMakeBorder(
            img, 0, 0, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # 图片宽高压缩
    img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_CUBIC)
    return img


# 创建数据集输出目录
os.makedirs(dataset_path, exist_ok=True)
for i in range(10):
    os.makedirs(dataset_path+'train/'+f'{i}', exist_ok=True)
    os.makedirs(dataset_path+'val/'+f'{i}', exist_ok=True)

# 获取(图像名, 标签)对
parsed_data = None
with open(input_dir+"labels.json", "r", encoding='utf-8') as file:
    data = eval(file.read())
    parsed_data = data["labels"]
data_pair = list(parsed_data.items())
# 随机打乱(图像, 标签)列表
random.shuffle(data_pair)

# print(data_pair)
# 确定测试集的图像数量（这里假设使用10%的图像作为测试集）
num_test_images = int(0.1 * len(data_pair))
# 复制测试集的图像到测试集的文件夹中
for i in range(num_test_images):
    img_name, labels = data_pair[i]
    input_img = input_dir+"images/"+img_name+'.jpg'
    output_img = dataset_path+'val/' + f'{labels}/'+img_name+'.jpg'
    img = cv2.imread(input_img)
    img = process_img(img)
    cv2.imwrite(output_img, img)
    # shutil.copy(input_img, output_img)

# 复制训练集的图像到训练集的文件夹中
for i in range(num_test_images, len(data_pair)):
    img_name, labels = data_pair[i]
    input_img = input_dir+"images/"+img_name+'.jpg'
    output_img = dataset_path+'train/' + f'{labels}/'+img_name+'.jpg'
    img = cv2.imread(input_img)
    img = process_img(img)
    cv2.imwrite(output_img, img)
    # shutil.copy(input_img, output_img)


# 打印图像数量
print("Total images: ", len(data_pair))
print("Num test images: ", num_test_images)
print("Num train images: ", len(data_pair) - num_test_images)
