import json
import os

# 指定存放JSON文件的文件夹路径
folder_path = r'E:\pig\train_json'

# 获取文件夹中所有的JSON文件
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]

def update_image_paths(file_paths):
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 如果'imagePath'字段存在，更新它只保留文件名
            if 'imagePath' in data:
                data['imagePath'] = os.path.basename(data['imagePath'])

        # 保存更新后的内容，覆盖原来的JSON文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

# 执行更新函数，处理文件
update_image_paths(file_paths)
