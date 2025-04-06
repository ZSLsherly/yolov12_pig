import json
import os
from pathlib import Path
import cv2

# 输入路径
json_dir = "../../dataset/pig/train_json"  # JSON 文件目录
images_dir = "../../dataset/pig/train_img"  # 图片目录
output_dir = "../../dataset/pig/labels"  # 输出的 YOLO 标签目录
os.makedirs(output_dir, exist_ok=True)

# 类别映射（可扩展）
class_map = {"pig": 0}  # 如果有多类别，可以添加，如 "cow": 1

# 遍历所有 JSON 文件
for json_file in Path(json_dir).glob("*.json"):
    try:
        with open(json_file, "r") as f:
            data = json.load(f)

        # 检查图片是否存在
        image_path = Path(images_dir) / f"{json_file.stem}.jpg"
        if not image_path.exists():
            print(f"⚠️ 图片不存在: {image_path}")
            continue

        # 获取图片尺寸（强制校验）
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"❌ 图片读取失败: {image_path}")
            continue
        image_height, image_width = img.shape[:2]

        # 收集有效标注
        valid_annotations = []

        # 遍历标注
        for item in data.get("shape", []):
            # 检查 boxes 是否存在且格式正确
            boxes = item.get("boxes")
            if boxes is None:
                print(f"⚠️ 跳过无效标注（boxes=None），文件: {json_file.stem}")
                continue
            if not isinstance(boxes, list) or len(boxes) != 4:
                print(f"⚠️ 跳过无效 boxes 格式，文件: {json_file.stem}")
                continue

            # 检查 label 是否有效
            label = item.get("label")
            class_id = class_map.get(label, -1)
            if class_id == -1:
                print(f"⚠️ 未知标签 '{label}'，文件: {json_file.stem}")
                continue

            # 校验坐标是否越界
            x1, y1, x2, y2 = boxes
            x1, y1 = max(0, x1), max(0, y1)  # 确保不小于 0
            x2, y2 = min(image_width, x2), min(image_height, y2)  # 确保不超过图片尺寸

            # 转换为 YOLO 格式（归一化）
            x_center = (x1 + x2) / 2 / image_width
            y_center = (y1 + y2) / 2 / image_height
            width = (x2 - x1) / image_width
            height = (y2 - y1) / image_height

            # 保存有效标注
            valid_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        # 仅在有有效标注时生成 .txt 文件
        if valid_annotations:
            txt_path = Path(output_dir) / f"{json_file.stem}.txt"
            with open(txt_path, "w") as f_txt:
                f_txt.write("\n".join(valid_annotations))
        else:
            print(f"⚠️ 无有效标注，跳过文件: {json_file.stem}")

    except Exception as e:
        print(f"❌ 处理文件 {json_file} 时出错: {e}")
        continue

print("✅ YOLO 标签转换完成！")