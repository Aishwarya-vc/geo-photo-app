from flask import Flask, render_template, request
from datetime import datetime
import os, base64, csv, json

# Google Sheets Setup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CSV_FILE = 'data.csv'

# Make sure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Setup Google Sheets using environment variable
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds_dict = json.loads(os.environ["GOOGLE_CREDS_JSON"])  # ✅ Render uses env var
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your sheet
sheet = client.open_by_key('1vb8KpLlP3lccrY_vts_csGBOs_OtX6HADY5U9DtE-9M').sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    emp_id = request.form['emp_id']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    image_data = request.form['image']

    # Decode image and save to uploads/
    format, imgstr = image_data.split(';base64,')
    image_bytes = base64.b64decode(imgstr)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{emp_id}_{timestamp}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, 'wb') as f:
        f.write(image_bytes)

    # Save to CSV
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([emp_id, latitude, longitude, timestamp, filename])

    # Save to Google Sheet
    sheet.append_row([emp_id, latitude, longitude, timestamp, filename])

    return '✅ Data submitted successfully'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
