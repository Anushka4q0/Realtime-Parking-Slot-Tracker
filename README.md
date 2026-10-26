# Realtime Parking Slot Tracker
This project provides a basic pipeline to detect and track the occupancy of parking slots in a static parking lot image using OpenCV.
## 📁 Project Structure

Realtime_parkingslot_tracker/
│
├── Scripts/
│ ├── parking_slot_marker.py # Marks the positions of parking slots and stores them
│ ├── parking_occupancy_detector.py # Detects occupied and available slots
│
├── parking_image/
│ └── parking_image.jpg.jpg # Aerial view of parking lot used for processing
│
├── park_positions # Serialized file with saved slot positions (using pickle)
├── parking_occupancy_report_*.xlsx # Auto-generated Excel reports of slot occupancy
├── README.md # Project description and usage


## ⚙️ Requirements

- Python (Ensure it's added to your system PATH)
- OpenCV
- Pandas

Install dependencies:
pip install opencv-python pandas


How It Works:
1. Define Parking Slots: python parking_slot_marker.py

Use left-click and drag to draw a row of parking slots on the image.

To delete a slot, right-click on it.

The marked slot coordinates are automatically stored in the park_positions file.

2. Analyze Slot Occupancy: pyhton parking_occupancy_detector.py

Shows the parking image with each slot visually marked:

🟩 Green indicates an empty slot

🟥 Red marks an occupied one

Generates an Excel file containing the occupancy summary, including the current timestamp.


