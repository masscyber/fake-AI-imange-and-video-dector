import cv2
import os
from .image_detector import analyze_image

def extract_frames(video_path, step=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    idx = 0
    success, frame = cap.read()
    while success:
        if idx % step == 0:
            frames.append(frame)
        idx += 1
        success, frame = cap.read()
    cap.release()
    return frames

def analyze_video(video_path):
    result = {'file': os.path.basename(video_path)}
    frames = extract_frames(video_path, step=25)
    frame_results = []
    import tempfile, shutil
    tdir = tempfile.mkdtemp()
    try:
        for i, f in enumerate(frames):
            p = os.path.join(tdir, f'frame_{i}.jpg')
            cv2.imwrite(p, f)
            r = analyze_image(p)
            frame_results.append(r)
    finally:
        try:
            shutil.rmtree(tdir)
        except Exception:
            pass
    fake_probs = [r['model']['fake_prob'] for r in frame_results if 'model' in r]
    avg_fake_prob = sum(fake_probs)/len(fake_probs) if fake_probs else 0.0
    result['avg_fake_prob'] = avg_fake_prob
    result['is_fake'] = avg_fake_prob > 0.5
    result['per_frame'] = frame_results
    return result
