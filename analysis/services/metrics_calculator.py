import numpy as np

class MetricsCalculator:
    def __init__(self):
        pass

    def calculate_metrics(self, frames_data, start_idx, end_idx):
        """
        Calculates swing metrics based on the swing range.
        """
        if not frames_data or start_idx >= end_idx:
            return {}

        swing_frames = frames_data[start_idx:end_idx+1]
        
        # 1. Swing Plane Consistency
        # We'll look at the variance of the hand path from a fitted line/plane
        # For 2D video, we can fit a line to (x, y) of hands
        hand_points = []
        for frame in swing_frames:
            kp = self._get_landmark_dict(frame)
            if 'right_wrist' in kp:
                hand_points.append([kp['right_wrist']['x'], kp['right_wrist']['y']])
        
        plane_score = 0
        if len(hand_points) > 5:
            points = np.array(hand_points)
            # Fit line: y = mx + c
            # We want distance from this line
            # Simple approach: standard deviation of residuals
            x = points[:, 0]
            y = points[:, 1]
            A = np.vstack([x, np.ones(len(x))]).T
            m, c = np.linalg.lstsq(A, y, rcond=None)[0]
            
            # Calculate distances
            distances = np.abs(m * x - y + c) / np.sqrt(m**2 + 1)
            variance = np.mean(distances)
            
            # Normalize to 0-100 (lower variance is better)
            # Heuristic: 0.05 variance is bad (0 score), 0.01 is good (100 score)
            plane_score = max(0, min(100, 100 - (variance * 2000)))

        # 2. Shoulder Rotation (at top of backswing)
        # Find top of backswing (highest hand point)
        top_idx = 0
        min_y = 1.0 # y increases downwards
        for i, frame in enumerate(swing_frames):
            kp = self._get_landmark_dict(frame)
            if 'right_wrist' in kp and kp['right_wrist']['y'] < min_y:
                min_y = kp['right_wrist']['y']
                top_idx = i
        
        rotation_angle = 0
        if top_idx < len(swing_frames):
            kp = self._get_landmark_dict(swing_frames[top_idx])
            if 'left_shoulder' in kp and 'right_shoulder' in kp:
                ls = kp['left_shoulder']
                rs = kp['right_shoulder']
                # Angle of vector (rs - ls) relative to horizontal
                dy = rs['y'] - ls['y']
                dx = rs['x'] - ls['x']
                angle = np.degrees(np.arctan2(dy, dx))
                rotation_angle = abs(angle)

        # 3. Tempo
        # Ratio of backswing frames to downswing frames
        # Top is top_idx relative to start of swing_frames
        # Impact is roughly where max velocity was, but let's approximate
        # Impact is usually near the end of the "downswing"
        # Let's assume impact is roughly 80% through the swing for now or find max vel again
        # Re-using max velocity logic would be better, but for now:
        backswing_frames = top_idx
        downswing_frames = len(swing_frames) - top_idx # Rough approx
        
        tempo_ratio = 0
        if downswing_frames > 0:
            tempo_ratio = backswing_frames / downswing_frames

        return {
            "plane_score": float(plane_score),
            "rotation_angle": float(rotation_angle),
            "tempo": float(tempo_ratio),
            "top_frame_relative": top_idx
        }

    def _get_landmark_dict(self, frame_data):
        # Helper similar to PoseEstimator's but we need it here too
        # Or we could have passed dicts. For now, duplication is fine for speed.
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
