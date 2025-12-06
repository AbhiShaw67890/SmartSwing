import numpy as np

class SwingDetector:
    def __init__(self):
        pass

    def detect_swing(self, frames_data):
        """
        Detects the start and end of a golf swing based on keypoint movement.
        Returns: (start_frame_idx, end_frame_idx)
        """
        if not frames_data:
            return 0, 0

        # Extract wrist velocities to find the "Impact" (max velocity)
        velocities = []
        for i in range(1, len(frames_data)):
            prev_frame = frames_data[i-1]['keypoints']
            curr_frame = frames_data[i]['keypoints']
            
            # Get right wrist (index 16) or left wrist (index 15)
            # We'll average both for robustness
            prev_rw = self._get_point(prev_frame, 16)
            curr_rw = self._get_point(curr_frame, 16)
            
            if prev_rw and curr_rw:
                dist = np.sqrt((curr_rw['x'] - prev_rw['x'])**2 + (curr_rw['y'] - prev_rw['y'])**2)
                velocities.append(dist)
            else:
                velocities.append(0)

        if not velocities:
            return 0, len(frames_data) - 1

        # 1. Find Impact (Max Velocity)
        # Smooth velocities slightly to avoid noise
        velocities = np.array(velocities)
        # simple moving average
        window_size = 3
        if len(velocities) > window_size:
            velocities = np.convolve(velocities, np.ones(window_size)/window_size, mode='same')
            
        impact_idx = np.argmax(velocities)
        
        # 2. Find Start (Address) - Search backwards from impact
        # Look for a period of low velocity (stillness) before the backswing starts
        start_idx = 0
        threshold_still = np.max(velocities) * 0.05 # 5% of max velocity
        
        for i in range(impact_idx, 0, -1):
            if velocities[i] < threshold_still:
                # Found a still point, but let's go back a bit more to be safe
                # or check if it stays still for a few frames
                start_idx = max(0, i - 10) 
                break
                
        # 3. Find End (Finish) - Search forwards from impact
        end_idx = len(frames_data) - 1
        for i in range(impact_idx, len(velocities)):
            if velocities[i] < threshold_still and i > impact_idx + 20:
                end_idx = min(len(frames_data) - 1, i + 10)
                break
                
        return start_idx, end_idx

    def _get_point(self, keypoints, idx):
        # keypoints is a list of dicts {x, y, z, visibility}
        # MediaPipe pose landmarks are 0-32
        if idx < len(keypoints):
            return keypoints[idx]
        return None
