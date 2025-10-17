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

        # 手臂弯曲计数相关变量
        self.left_arm_bend_count = 0
        self.right_arm_bend_count = 0
        self.left_arm_prev_state = "straight"  # 初始状态为伸直
        self.right_arm_prev_state = "straight"  # 初始状态为伸直

        # 手臂关键点索引
        self.LEFT_SHOULDER = 12
        self.LEFT_ELBOW = 14
        self.LEFT_WRIST = 16
        self.RIGHT_SHOULDER = 11
        self.RIGHT_ELBOW = 13
        self.RIGHT_WRIST = 15

        # 弯曲角度阈值
        self.BEND_ANGLE_THRESHOLD = 120  # 小于这个角度认为是弯曲
        self.STRAIGHT_ANGLE_THRESHOLD = 160  # 大于这个角度认为是伸直

    def calculate_angle(self, a, b, c):
        """
        计算三个点形成的角度

        参数:
            a, b, c: 三个点的坐标，每个点包含x,y坐标

        返回:
            angle: 三个点形成的角度（度数）
        """
        import math

        # 计算向量ba和bc
        ba = [a[0] - b[0], a[1] - b[1]]
        bc = [c[0] - b[0], c[1] - b[1]]

        # 计算点积
        dot_product = ba[0] * bc[0] + ba[1] * bc[1]

        # 计算模长
        magnitude_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
        magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

        # 计算夹角余弦值
        if magnitude_ba * magnitude_bc == 0:
            return 180

        cosine_angle = dot_product / (magnitude_ba * magnitude_bc)

        # 防止数值误差导致超出[-1, 1]范围
        cosine_angle = max(-1, min(1, cosine_angle))

        # 计算角度（度数）
        angle = math.degrees(math.acos(cosine_angle))

        return angle

    def arm_bend_detect(self, pose_landmarks, frame):
        """
        通过使用12、14、16关键点进行手臂弯曲的次数统计

        参数:
            pose_landmarks: 姿势关键点数据
            frame: 图像帧（用于绘制信息）

        返回:
            frame: 添加了手臂弯曲信息的图像帧
        """
        if pose_landmarks is None:
            return frame

        # 获取所有关键点
        landmarks = pose_landmarks.landmark

        # 获取左手臂关键点坐标
        left_shoulder = [landmarks[self.LEFT_SHOULDER].x, landmarks[self.LEFT_SHOULDER].y]
        left_elbow = [landmarks[self.LEFT_ELBOW].x, landmarks[self.LEFT_ELBOW].y]
        left_wrist = [landmarks[self.LEFT_WRIST].x, landmarks[self.LEFT_WRIST].y]

        # 获取右手臂关键点坐标
        right_shoulder = [landmarks[self.RIGHT_SHOULDER].x, landmarks[self.RIGHT_SHOULDER].y]
        right_elbow = [landmarks[self.RIGHT_ELBOW].x, landmarks[self.RIGHT_ELBOW].y]
        right_wrist = [landmarks[self.RIGHT_WRIST].x, landmarks[self.RIGHT_WRIST].y]

        # 计算左手臂角度
        left_arm_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)

        # 计算右手臂角度
        right_arm_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)

        # 检测左手臂弯曲状态变化
        if left_arm_angle < self.BEND_ANGLE_THRESHOLD and self.left_arm_prev_state == "straight":
            self.left_arm_bend_count += 1
            self.left_arm_prev_state = "bent"
        elif left_arm_angle > self.STRAIGHT_ANGLE_THRESHOLD and self.left_arm_prev_state == "bent":
            self.left_arm_prev_state = "straight"

        # 检测右手臂弯曲状态变化
        if right_arm_angle < self.BEND_ANGLE_THRESHOLD and self.right_arm_prev_state == "straight":
            self.right_arm_bend_count += 1
            self.right_arm_prev_state = "bent"
        elif right_arm_angle > self.STRAIGHT_ANGLE_THRESHOLD and self.right_arm_prev_state == "bent":
            self.right_arm_prev_state = "straight"

        # 在图像上显示手臂弯曲信息
        cv2.putText(frame, f"Left Arm Bends: {self.left_arm_bend_count}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Right Arm Bends: {self.right_arm_bend_count}",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Left Angle: {left_arm_angle:.1f}",
                    (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.putText(frame, f"Right Angle: {right_arm_angle:.1f}",
                    (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        return frame

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

        # 手臂弯曲检测
        frame = self.arm_bend_detect(pose_landmarks, frame)

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