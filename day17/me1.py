# 手部关键点检测

import mediapipe as mp
import cv2

class Hand:
    def __init__(self):
        self.frame

        """
        初始化手部检测器
        在类的构造函数中创建MediaPipe手部模型实例
        """
        # 创建MediaPipe手部检测模型实例
        # Hands() 默认参数：
        # - static_image_mode: False (适用于视频流，会使用跟踪来优化性能)
        # - max_num_hands: 2 (最多检测2只手)
        # - min_detection_confidence: 0.5 (检测置信度阈值)
        # - min_tracking_confidence: 0.5 (跟踪置信度阈值)
        self.hands = mp.solutions.hands.Hands()

        # 创建绘图工具实例，用于在图像上绘制关键点和连接线
        self.mp_drawing = mp.solutions.drawing_utils

    def process(self):
        """
        主处理函数：打开摄像头，实时检测并显示手部关键点
        """
        # 打开默认摄像头（摄像头索引0代表系统默认摄像头）
        cap = cv2.VideoCapture(0)

        # 检查摄像头是否成功打开
        if not cap.isOpened():
            print("错误：无法打开摄像头")
            return

        # 进入主循环，持续处理视频帧
        while cap.isOpened():
            # 读取一帧图像
            # ret: 读取是否成功的布尔值 (True/False)
            # frame: 读取到的图像帧 (BGR格式)
            ret, self.frame = cap.read()

            # 如果读取失败，退出循环
            if not ret:
                print("错误：无法读取视频帧")
                break

            # 水平翻转图像，使显示效果更自然（像镜子一样）
            # 参数1: 输入图像
            # 参数2: 翻转方向 (1: 水平翻转, 0: 垂直翻转, -1: 水平垂直都翻转)
            frame = cv2.flip(frame, 1)

            # 将BGR格式转换为RGB格式
            # MediaPipe模型需要RGB格式的输入图像
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 使用MediaPipe手部模型处理图像
            # process()方法接收RGB图像，返回检测结果
            result = self.hands.process(frame_rgb)

            # 检查是否检测到手部关键点
            # result.multi_hand_landmarks 是一个列表，包含所有检测到的手的关键点
            if result.multi_hand_landmarks:
                # 获取第一只手的关键点信息
                # multi_hand_landmarks[0] 代表检测到的第一只手
                first_hand = result.multi_hand_landmarks[0]

                # 在图像上绘制手部关键点和连接线
                # 参数1: 要绘制到的目标图像 (BGR格式)
                # 参数2: 手部关键点数据
                # 参数3: 手部关键点之间的连接关系 (预定义的连接线)
                self.mp_drawing.draw_landmarks(
                    frame,  # 目标图像
                    first_hand,  # 手部关键点数据
                    mp.solutions.hands.HAND_CONNECTIONS  # 预定义的手部连接线
                )

                # 可选：在控制台打印检测状态
                # print("检测到手部，正在绘制关键点...")

            # 显示处理后的图像
            # 窗口标题: 'First Hand Only'
            cv2.imshow('First Hand Only', frame)

            # 等待键盘输入，延迟1毫秒
            # 按ESC键(ASCII码27)退出程序
            # waitKey(1) 返回按键的ASCII码，& 0xFF 是为了兼容64位系统
            if cv2.waitKey(1) & 0xFF == 27:
                print("用户按ESC键退出")
                break

        # 释放摄像头资源
        cap.release()

        # 关闭所有OpenCV创建的窗口
        cv2.destroyAllWindows()

        print("程序正常退出")

    def gesture_num_detect(self):
        cap = cv2.VideoCapture(0)

        # 检查摄像头是否成功打开
        if not cap.isOpened():
            print("错误：无法打开摄像头")
            return

        # 进入主循环，持续处理视频帧
        while cap.isOpened():
            # 读取一帧图像
            # ret: 读取是否成功的布尔值 (True/False)
            # frame: 读取到的图像帧 (BGR格式)
            ret, self.frame = cap.read()

            # 如果读取失败，退出循环
            if not ret:
                print("错误：无法读取视频帧")
                break

            # 水平翻转图像，使显示效果更自然（像镜子一样）
            # 参数1: 输入图像
            # 参数2: 翻转方向 (1: 水平翻转, 0: 垂直翻转, -1: 水平垂直都翻转)
            frame = cv2.flip(frame, 1)

            # 将BGR格式转换为RGB格式
            # MediaPipe模型需要RGB格式的输入图像
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 使用MediaPipe手部模型处理图像
            # process()方法接收RGB图像，返回检测结果
            result = self.hands.process(frame_rgb)

            # 检查是否检测到手部关键点
            # result.multi_hand_landmarks 是一个列表，包含所有检测到的手的关键点
            if result.multi_hand_landmarks:
                # 获取第一只手的关键点信息
                # multi_hand_landmarks[0] 代表检测到的第一只手
                first_hand = result.multi_hand_landmarks[0]

                # 在图像上绘制手部关键点和连接线
                # 参数1: 要绘制到的目标图像 (BGR格式)
                # 参数2: 手部关键点数据
                # 参数3: 手部关键点之间的连接关系 (预定义的连接线)
                self.mp_drawing.draw_landmarks(
                    frame,  # 目标图像
                    first_hand,  # 手部关键点数据
                    mp.solutions.hands.HAND_CONNECTIONS  # 预定义的手部连接线
                )

                # 可选：在控制台打印检测状态
                # print("检测到手部，正在绘制关键点...")

            # 显示处理后的图像
            # 窗口标题: 'First Hand Only'
            cv2.imshow('First Hand Only', frame)

            # 等待键盘输入，延迟1毫秒
            # 按ESC键(ASCII码27)退出程序
            # waitKey(1) 返回按键的ASCII码，& 0xFF 是为了兼容64位系统
            if cv2.waitKey(1) & 0xFF == 27:
                print("用户按ESC键退出")
                break

        # 释放摄像头资源
        cap.release()

        # 关闭所有OpenCV创建的窗口
        cv2.destroyAllWindows()

        print("程序正常退出")

        pass


if __name__ == "__main__":
    Hand().process()