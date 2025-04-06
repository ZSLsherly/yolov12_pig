import os
import json

def update_shapes_to_shape(json_folder):
    """
    处理指定文件夹中的所有JSON文件，将其中的'shapes'字段改为'shape'。
    """
    # 获取所有的JSON文件
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]

    for json_file in json_files:
        file_path = os.path.join(json_folder, json_file)
        
        # 读取JSON数据
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 如果存在'shapes'字段，则将其改为'shape'
        if 'shapes' in data:
            data['shape'] = data.pop('shapes')
        
        # 将修改后的JSON数据保存回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"已处理文件: {json_file}")

# 指定存放JSON文件的文件夹路径
json_folder_path = 'E:/pig/train_json'  # 将此路径替换为你的实际路径

# 调用函数处理JSON文件
update_shapes_to_shape(json_folder_path)
