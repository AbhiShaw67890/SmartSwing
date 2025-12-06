# SmartSwing ⛳

SmartSwing is an AI-powered web application for analyzing golf swings. It uses computer vision to extract body mechanics from video and provides actionable feedback to improve your game.

## Key Features
*   **AI Pose Estimation**: Tracks 33 body keypoints to understand your movement using MediaPipe.
*   **Swing Detection**: Automatically identifies Address, Impact, and Follow-through phases.
*   **Smart Metrics**: Calculates critical metrics like Swing Plane, Shoulder Rotation, and Tempo.
*   **Scoring System**: Generates a 0-100 accuracy score with specific error detection (e.g., "Early Extension").
*   **Visual Feedback**: Overlays a dynamic skeleton on your video for visual analysis.

## Tech Stack
*   **Backend**: Python, Django, Django REST Framework
*   **ML/CV**: MediaPipe, OpenCV, NumPy
*   **Frontend**: HTML5, CSS3, JavaScript (Canvas API)

## How to Run

1.  **Install Dependencies**:
    ```bash
    pip install django djangorestframework opencv-python mediapipe markdown django-filter
    ```

2.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

3.  **Start the Server**:
    ```bash
    python manage.py runserver
    ```

4.  **Access the App**:
    *   Open your browser to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    *   **Mobile**: Use your PC's local IP (e.g., `http://192.168.1.X:8000/`) while on the same Wi-Fi.

## Usage
1.  **Upload**: Select a video file or record one directly from your phone.
2.  **Analyze**: The system processes the video in the background (Pose Estimation -> Swing Detection -> Scoring).
3.  **Results**: View your Swing Score, detailed metrics, and a visual overlay of your swing plane and body segments.