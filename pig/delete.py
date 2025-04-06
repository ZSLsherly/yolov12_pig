import os

# 指定存放多余JSON文件的文件夹路径
folder_path = r'E:\pig\train_json'

# 获取所有以 _updated.json 和 _updated_updated.json 结尾的文件
files_to_delete = [f for f in os.listdir(folder_path) if f.endswith('_updated.json') or f.endswith('_updated_updated.json')]

# 删除这些文件
for file in files_to_delete:
    file_path = os.path.join(folder_path, file)
    try:
        os.remove(file_path)
        print(f'已删除文件: {file_path}')
    except Exception as e:
        print(f'删除文件 {file_path} 时发生错误: {e}')
