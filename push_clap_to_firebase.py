import serial
import time
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# CONFIG: update these paths and ports
SERIAL_PORT = 'COM4'             # Change to your Arduino serial port
BAUD_RATE = 9600
SERVICE_ACCOUNT_FILE = 'secrets.json'  # Your Firebase Admin SDK JSON file
DATABASE_URL = 'https://tap-detection-default-rtdb.firebaseio.com/'             # Your Firebase DB URL

# Initialize Firebase Admin SDK
cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred, {
    'databaseURL': DATABASE_URL
})

# Open serial port
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # wait for Arduino reset
    print(f"Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    print("Failed to open serial port:", e)
    exit(1)

# Firebase DB reference
clap_ref = db.reference('clap')

def push_clap(count):
    data = {
        'count': count,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    clap_ref.set(data)
    print(f"Pushed to Firebase: {data}")

# Main loop: read serial and push to Firebase
try:
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line.isdigit():
            clapCount = int(line)
            push_clap(clapCount)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping...")
    ser.close()
