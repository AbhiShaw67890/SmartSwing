class Scorer:
    def __init__(self):
        pass

    def compute_score(self, metrics):
        """
        Computes final score and error flags.
        """
        if not metrics:
            return 0, []

        # Weights
        w_plane = 0.4
        w_rotation = 0.3
        w_tempo = 0.3

        # Normalize Rotation (Ideal ~90 deg, acceptable > 45)
        rot = metrics.get('rotation_angle', 0)
        rot_score = min(100, (rot / 90.0) * 100)
        
        # Normalize Tempo (Ideal 3.0)
        tempo = metrics.get('tempo', 0)
        # Score drops off as we move away from 3.0
        tempo_diff = abs(tempo - 3.0)
        tempo_score = max(0, 100 - (tempo_diff * 30))

        plane_score = metrics.get('plane_score', 0)

        final_score = (plane_score * w_plane) + \
                      (rot_score * w_rotation) + \
                      (tempo_score * w_tempo)

        errors = []
        if plane_score < 50:
            errors.append({
                "id": "off_plane", 
                "severity": "medium", 
                "message": "Your swing plane is inconsistent."
            })
        if rot_score < 50:
            errors.append({
                "id": "limited_turn", 
                "severity": "medium", 
                "message": "Try to rotate your shoulders more in the backswing."
            })
        if tempo < 2.0:
            errors.append({
                "id": "fast_tempo", 
                "severity": "low", 
                "message": "Your backswing is too fast relative to downswing."
            })

        return int(final_score), errors
