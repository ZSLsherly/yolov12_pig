from ultralytics import YOLO

if __name__=='__main__':
    # 加载训练好的模型
    model = YOLO("runs/detect/yolov12_pig/weights/epoch90.pt")  # 替换为你的模型路径

    # 预测单张图片（仅可视化结果）
    results = model.predict(
        source="test.jpg",  # 替换为你的图片路径
        imgsz=(512, 680),
        conf=0.01,                    # 置信度阈值
        save=True,                  # 保存预测结果
        save_txt=False,              # 不保存标签文件（因为没有真实标签）
        show_labels=True,            # 显示标签
        show_conf=True               # 显示置信度
    )
    results = model.predict(source="pig.jpg", save=False)
    boxes = results[0].boxes  # 检测框信息
    print(boxes.xyxy)  # 检测框坐标 (x1, y1, x2, y2)
    print(boxes.conf)  # 置信度
    print(boxes.cls)   # 类别ID