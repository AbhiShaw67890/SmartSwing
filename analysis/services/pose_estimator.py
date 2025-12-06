import cv2
import mediapipe as mp
import numpy as np

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process_video(self, video_path):
        """
        Processes a video file and extracts pose landmarks for each frame.
        Returns a list of frames, where each frame is a list of landmarks.
        """
        cap = cv2.VideoCapture(video_path)
        frames_data = []
        frame_idx = 0

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            # Convert the BGR image to RGB.
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process the image and find poses
            results = self.pose.process(image_rgb)
            
            frame_landmarks = []
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    frame_landmarks.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z,
                        'visibility': landmark.visibility
                    })
            
            frames_data.append({
                'frame_idx': frame_idx,
                'keypoints': frame_landmarks
            })
            frame_idx += 1

        cap.release()
        return frames_data

    def get_landmark_dict(self, frame_data):
        """
        Helper to convert list of landmarks to a dict keyed by name for easier access.
        """
        if not frame_data or 'keypoints' not in frame_data:
            return {}
            
        # Map indices to names (subset of important ones)
        # https://developers.google.com/mediapipe/solutions/vision/pose
        names = {
            11: 'left_shoulder', 12: 'right_shoulder',
            13: 'left_elbow', 14: 'right_elbow',
            15: 'left_wrist', 16: 'right_wrist',
            23: 'left_hip', 24: 'right_hip',
            25: 'left_knee', 26: 'right_knee',
            27: 'left_ankle', 28: 'right_ankle'
        }
        
        result = {}
        kp = frame_data['keypoints']
        for idx, name in names.items():
            if idx < len(kp):
                result[name] = kp[idx]
        return result
