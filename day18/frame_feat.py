import cv2
import mediapipe as mp
import numpy as np

class FrameFeat:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        pass

    def get_pose_landmark(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        pose_landmarks = results.pose_landmarks
        if pose_landmarks is None:
            return
        keypoint = []
        for lm in pose_landmarks.landmark:
            keypoint.append((lm.x, lm.y))

        keypoint = np.array(keypoint).flatten()
        return keypoint
        pass

    def get_frame_feat(self):
        """
        获取特征
        """
        feat = self.get_pose_landmark(frame)
        if feat is None:
            print("feature is not exist")
        return feat
        pass

    def load_db_feat(self):
        """
        加载已存储的特征
        """
        pass



if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame_feat = FrameFeat()
    frame_feat.get_pose_landmark(frame)

    pass