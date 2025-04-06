from ultralytics import YOLO
import torch


def main():
    # 设备检测
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 加载模型
    model = YOLO("yolov12n.pt").to(device)

    # 训练配置
    results = model.train(
        data="pig_dataset.yaml",
        epochs=100,
        batch=16,
        imgsz=(512,680),
        device=device,
        val=True,
        # validate=False,
        name="yolov12_pig",
        save_period=10,
        workers=0
    )

if __name__ == "__main__":
    main()