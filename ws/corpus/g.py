import random

random_numbers = [random.randint(0, 9) for _ in range(3000)]

# 将数字列表转换为字符串
numbers_str = ''.join(str(num)+' ' for num in random_numbers)

# 写入文件
file_path = './text.txt'
with open(file_path, 'w') as file:
    file.write(numbers_str)

print(f"随机数字已写入文件: {file_path}")
