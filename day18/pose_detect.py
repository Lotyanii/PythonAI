import mediapipe as mp
import cv2


class PoseProcess:
    def __init__(self):
        """
        初始化姿势检测器
        使用mediapipe的Pose模型进行人体姿势关键点检测
        """
        # 初始化mediapipe姿势检测模型
        self.pose = mp.solutions.pose.Pose()
        pass

    def get_pose_landmark(self, frame_rgb):
        """
        获取姿势关键点

        参数:
            frame_rgb: RGB格式的图像帧

        返回:
            result: 包含姿势关键点检测结果的对象
        """
        # 使用mediapipe姿势模型处理RGB图像帧
        result = self.pose.process(frame_rgb)
        return result

    def draw_style(self, frame, pose_landmarks):
        """
        绘制关键点和连接线的样式

        参数:
            frame: 原始BGR图像帧
            pose_landmarks: 姿势关键点数据

        返回:
            frame: 绘制了关键点和连接线后的图像帧
        """
        # 定义姿势关键点之间的连接关系
        connections = mp.solutions.pose.POSE_CONNECTIONS

        # 设置关键点的绘制样式：黑色，厚度为2
        point_style = mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 0), thickness=2)
        # 设置连接线的绘制样式：白色，厚度为2
        line_style = mp.solutions.drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=2)

        # 在图像上绘制姿势关键点和连接线
        mp.solutions.drawing_utils.draw_landmarks(
            frame,  # 要绘制的图像
            pose_landmarks,  # 姿势关键点数据
            connections,  # 关键点连接关系
            point_style,  # 关键点样式
            line_style  # 连接线样式
        )

        return frame

    def process(self, frame):
        """
        处理图像帧，检测并绘制姿势关键点

        参数:
            frame: 输入的BGR图像帧

        返回:
            frame: 处理后的图像帧（包含绘制的关键点和编号）
        """
        # 将BGR图像转换为RGB格式，因为mediapipe需要RGB输入
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 获取姿势关键点检测结果
        result = self.get_pose_landmark(frame_rgb)

        # 提取姿势关键点数据
        pose_landmarks = result.pose_landmarks

        # 如果没有检测到姿势关键点，直接返回原图像
        if pose_landmarks is None:
            return frame

        # 绘制关键点和连接线的样式
        frame = self.draw_style(frame, pose_landmarks)

        # 获取所有关键点的列表
        landmark = pose_landmarks.landmark

        # 遍历所有关键点，为每个关键点添加编号标签
        for idx, lm in enumerate(landmark):
            # 将归一化的坐标转换为图像像素坐标
            x = int(lm.x * frame.shape[1])  # x坐标：归一化值 × 图像宽度
            y = int(lm.y * frame.shape[0])  # y坐标：归一化值 × 图像高度

            # 在关键点位置附近添加编号文本
            cv2.putText(
                frame,  # 要绘制的图像
                str(idx),  # 关键点编号文本
                (x - 5, y),  # 文本位置（关键点左侧5像素）
                cv2.FONT_ITALIC,  # 字体样式
                0.6,  # 字体大小
                (0, 255, 0),  # 字体颜色（绿色）
                1  # 字体粗细
            )

        return frame

        pass