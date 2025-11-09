from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from werkzeug.utils import secure_filename
from detection.image_detector import analyze_image
from detection.video_detector import analyze_video

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_IMAGE = {'png','jpg','jpeg'}
ALLOWED_VIDEO = {'mp4','mov','avi'}

USERS = {'test@example.com': 'password123'}

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    pwd = request.form.get('password')
    if email in USERS and USERS[email] == pwd:
        session['user'] = email
        return redirect(url_for('dashboard'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return jsonify({'error':'unauthenticated'}), 401
    file = request.files.get('file')
    if not file:
        return jsonify({'error':'no file'}), 400
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.',1)[-1].lower()
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    if ext in ALLOWED_IMAGE:
        result = analyze_image(path)
    elif ext in ALLOWED_VIDEO:
        result = analyze_video(path)
    else:
        return jsonify({'error':'unsupported file type'}), 400

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
