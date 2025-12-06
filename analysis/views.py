from django.shortcuts import render
from rest_framework import viewsets
from .models import Swing
from .serializers import SwingSerializer
from .services.pose_estimator import PoseEstimator
from .services.swing_detector import SwingDetector
from .services.metrics_calculator import MetricsCalculator
from .services.scorer import Scorer
import threading
import numpy as np
import logging

logger = logging.getLogger(__name__)

def convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    return obj

class SwingViewSet(viewsets.ModelViewSet):
    queryset = Swing.objects.all().order_by('-created_at')
    serializer_class = SwingSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        # Run analysis in a separate thread to not block the response completely
        # (Though for a true async experience we'd need Celery, this is fine for a prototype)
        thread = threading.Thread(target=self.run_analysis, args=(instance,))
        thread.start()

    def run_analysis(self, instance):
        try:
            print(f"Starting analysis for Swing {instance.id}...")
            estimator = PoseEstimator()
            # instance.video.path gives the absolute path
            frames_data = estimator.process_video(instance.video.path)
            
            # Detect Swing
            detector = SwingDetector()
            start_idx, end_idx = detector.detect_swing(frames_data)

            # Calculate Metrics
            metrics_calc = MetricsCalculator()
            metrics = metrics_calc.calculate_metrics(frames_data, start_idx, end_idx)

            # Compute Score
            scorer = Scorer()
            score, errors = scorer.compute_score(metrics)

            # Save results
            raw_data = {
                'frames': frames_data,
                'swing_range': [start_idx, end_idx],
                'metrics': metrics,
                'score': score,
                'errors': errors,
                'metadata': {
                    'frame_count': len(frames_data),
                    'fps': 30 # Assumption for now, or get from cv2
                }
            }
            
            # Convert numpy types to native python types for JSON serialization
            instance.analysis_data = convert_numpy(raw_data)
            instance.processed = True
            instance.save()
            print(f"Analysis complete for Swing {instance.id}")
        except Exception as e:
            import traceback
            print(f"Error analyzing Swing {instance.id}: {e}")
            traceback.print_exc()
            # Optionally save error state to model if you add an error field


def upload_page(request):
    return render(request, 'upload.html')

def results_page(request, swing_id):
    return render(request, 'results.html', {'swing_id': swing_id})

