import os
import shutil
import random
from tqdm import tqdm


def split_dataset(
        source_img_dir,  # 原始图片目录（包含所有图片）
        source_label_dir,  # 原始标签目录（包含所有.txt标签）
        output_dir,  # 输出根目录
        train_ratio=0.9,  # 训练集比例
        val_ratio=0.1,  # 验证集比例
        seed=42  # 随机种子
):
    """
    分割数据集为train/val，并自动创建YOLO所需的目录结构
    """
    # 设置随机种子
    random.seed(seed)

    # 创建输出目录结构
    os.makedirs(os.path.join(output_dir, "images", "train"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "images", "val"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "labels", "train"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "labels", "val"), exist_ok=True)

    # 获取所有图片文件（过滤非图片格式）
    img_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.dng', '.webp', '.mpo'}
    image_files = [f for f in os.listdir(source_img_dir)
                   if os.path.splitext(f)[1].lower() in img_formats]

    # 检查是否有对应的标签文件
    valid_pairs = []
    for img_file in image_files:
        label_file = os.path.splitext(img_file)[0] + '.txt'
        label_path = os.path.join(source_label_dir, label_file)
        if os.path.exists(label_path):
            valid_pairs.append((img_file, label_file))
        else:
            print(f"警告：图片 {img_file} 没有对应的标签文件")

    # 随机打乱
    random.shuffle(valid_pairs)

    # 计算分割点
    total = len(valid_pairs)
    train_end = int(total * train_ratio)

    # 复制文件函数
    def copy_files(file_pairs, img_dest, label_dest):
        for img_file, label_file in tqdm(file_pairs, desc="处理中"):
            # 复制图片
            shutil.copy(
                os.path.join(source_img_dir, img_file),
                os.path.join(img_dest, img_file)
            )
            # 复制标签
            shutil.copy(
                os.path.join(source_label_dir, label_file),
                os.path.join(label_dest, label_file)
            )

    # 分割数据集
    print(f"\n总样本数: {total} | 训练集: {train_end} | 验证集: {total - train_end}")
    copy_files(valid_pairs[:train_end],
               os.path.join(output_dir, "images", "train"),
               os.path.join(output_dir, "labels", "train"))
    copy_files(valid_pairs[train_end:],
               os.path.join(output_dir, "images", "val"),
               os.path.join(output_dir, "labels", "val"))

    # 生成YAML配置文件
    yaml_content = f"""train: {os.path.abspath(os.path.join(output_dir, 'images/train'))}
val: {os.path.abspath(os.path.join(output_dir, 'images/val'))}
nc: 1  # 修改为你的类别数
names: ['pig']  # 修改为你的类别名称
"""
    with open(os.path.join(output_dir, "dataset.yaml"), 'w') as f:
        f.write(yaml_content)

    print(f"\n数据集分割完成！YAML配置文件已生成: {os.path.join(output_dir, 'dataset.yaml')}")
    print(f"输出目录结构:")
    print(f"├── images/")
    print(f"│   ├── train/  # {len(valid_pairs[:train_end])}张训练图片")
    print(f"│   └── val/    # {len(valid_pairs[train_end:])}张验证图片")
    print(f"├── labels/")
    print(f"│   ├── train/  # {len(valid_pairs[:train_end])}个训练标签")
    print(f"│   └── val/    # {len(valid_pairs[train_end:])}个验证标签")
    print(f"└── dataset.yaml")


if __name__ == "__main__":
    # 配置参数（根据你的实际情况修改）
    config = {
        "source_img_dir": "train_img",  # 原始图片目录
        "source_label_dir": "labels",  # 原始标签目录
        "output_dir": ".",  # 输出目录
        "train_ratio": 0.9,  # 训练集比例
        "val_ratio": 0.1,  # 验证集比例
    }

    # 执行分割
    split_dataset(**config)