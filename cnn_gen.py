import random
import os
import shutil

input_dir = "./ws/output/"
dataset_path = './datasets/'

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
    shutil.copy(input_img, output_img)

# 复制训练集的图像到训练集的文件夹中
for i in range(num_test_images, len(data_pair)):
    img_name, labels = data_pair[i]
    input_img = input_dir+"images/"+img_name+'.jpg'
    output_img = dataset_path+'train/' + f'{labels}/'+img_name+'.jpg'
    shutil.copy(input_img, output_img)


# 打印图像数量
print("Total images: ", len(data_pair))
print("Num test images: ", num_test_images)
print("Num train images: ", len(data_pair) - num_test_images)
