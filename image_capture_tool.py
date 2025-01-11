import cv2
import os

from Ui_image_capture_tool import Ui_ImageCaptureTool

# 初始化摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 设置保存照片的目录
save_dir = "/home/jetson/Desktop/yolov5-5/data/images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

photo_counter = 0

while True:
    # 读取摄像头图像
    ret, frame = cap.read()
    # 如果读取成功，ret 为 True
    if not ret:
        print("无法从摄像头读取图像")
        break

    # 显示原始捕获的图像
    cv2.imshow('Camera Stream', frame)

    # 按 'q' 键退出循环，按 's' 键保存照片
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        # 生成照片文件名
        photo_filename = os.path.join(save_dir, f'test_12.16{photo_counter:04d}.jpg')
        # 保存原始照片
        cv2.imwrite(photo_filename, frame)
        print(f"照片已保存: {photo_filename}")
        photo_counter += 1

# 释放摄像头资源
cap.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()