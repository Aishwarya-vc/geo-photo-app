from flask import Flask, render_template, request
from datetime import datetime
import os, base64, csv

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CSV_FILE = 'data.csv'

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    emp_id = request.form['emp_id']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    image_data = request.form['image']

    # Decode base64 image
    format, imgstr = image_data.split(';base64,')
    image_bytes = base64.b64decode(imgstr)

    # Create a timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{emp_id}_{timestamp}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save image
    with open(filepath, 'wb') as f:
        f.write(image_bytes)

    # Save data to CSV
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([emp_id, latitude, longitude, timestamp, filename])

    return '✅ Data submitted successfully'

if __name__ == '__main__':
    # Bind to 0.0.0.0 and use environment port for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
