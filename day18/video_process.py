import cv2
import pose_detect as pd


class VideoProcess:
    def __init__(self):
        """
        初始化视频处理类
        负责摄像头视频流的捕获和姿势检测处理
        """
        # 初始化姿势检测处理器
        self.pose_detect = pd.PoseProcess()
        # 初始化摄像头，0表示默认摄像头
        self.cap = cv2.VideoCapture(0)
        pass

    def process(self):
        """
        主处理循环
        持续从摄像头读取帧并进行姿势检测处理
        """
        # 检查摄像头是否成功打开
        while self.cap.isOpened():
            # 读取摄像头帧
            # ret: 读取是否成功的标志（True/False）
            # frame: 读取到的图像帧
            ret, frame = self.cap.read()

            # 如果读取失败，跳过本次循环继续下一次读取
            if not ret:
                continue

            # 水平翻转帧，使画面呈现镜像效果（更符合用户习惯）
            frame = cv2.flip(frame, 1)

            # 调用姿势检测处理器进行肢体关键点检测
            # 该方法会在图像上绘制姿势关键点和连接线
            frame = self.pose_detect.process(frame)

            # 如果处理后的帧为空，跳过显示继续下一次处理
            if frame is None:
                continue

            # 在窗口中显示处理后的图像帧
            # 窗口标题为 'frame'
            cv2.imshow('frame', frame)

            # 等待键盘输入，25毫秒刷新一次
            # 这样可以控制视频播放速度并响应按键
            key = cv2.waitKey(25)

            # 如果按下 'q' 键，退出循环
            if key == ord('q'):
                break
            pass

        # 释放摄像头资源
        self.cap.release()
        # 关闭所有OpenCV创建的窗口
        cv2.destroyAllWindows()


if __name__ == '__main__':
    """
    程序主入口
    当直接运行此文件时执行以下代码
    """
    # 创建视频处理实例
    video_process = VideoProcess()
    # 开始视频处理流程
    video_process.process()