How to Run
Install Dependencies (if not already done):

```bash
pip install django djangorestframework opencv-python mediapipe markdown django-filter
```
Run Migrations:

```bash
python manage.py migrate
```

Start the Server:

```bash
python manage.py runserver
```


Access the App:

- Open your browser to http://127.0.0.1:8000/
- On mobile, ensure your phone is on the same network and use your PC's IP address (e.g., http://192.168.1.X:8000/).
- Usage Flow
- Upload: Click "Choose File" to select a video or "Capture" to record one.
- Analyze: Click "Analyze Swing". The video will upload and processing will start in the background.
- Results: You will be redirected to the results page.
- If analysis is still running, you'll see a "Loading..." message. Refresh after a few seconds.
- Once complete, you'll see your Score, Metrics, and the Video with the skeleton overlay.