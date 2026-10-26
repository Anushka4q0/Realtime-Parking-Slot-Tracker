import cv2
import pickle
import pandas as pd
from datetime import datetime

parking_image_path = 'parking_image/parking_image.jpg.jpg'
frame = cv2.imread(parking_image_path)
if frame is None:
    raise FileNotFoundError(f"Image not found at {parking_image_path}")

with open('park_positions', 'rb') as f:
    park_positions = pickle.load(f)

font = cv2.FONT_HERSHEY_COMPLEX_SMALL

w, h = 40, 19
full = w * h
empty = 0.10  

def parking_occupancy_detector(img_processed):
    global counter, occupied_counter
    counter = 0  
    occupied_counter = 0 
    
    for position in park_positions:
        x, y = position
        img_crop = img_processed[y:y + h, x:x + w]
        count = cv2.countNonZero(img_crop)
        ratio = count / full
        
        if ratio < empty:
            color = (0, 255, 0) 
            counter += 1
        else:
            color = (0, 0, 255) 
            occupied_counter += 1
            
        cv2.rectangle(overlay, position, (position[0] + w, position[1] + h), color, -1)
        cv2.putText(overlay, "{:.2f}".format(ratio), (x + 4, y + h - 4), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

overlay = frame.copy()
img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

parking_occupancy_detector(img_thresh)

alpha = 0.7
frame_new = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

total_slots = 396  
occupied_slots = occupied_counter
available_slots = total_slots - occupied_slots

data = {
    'Category': ['Total Slots', 'Occupied Slots', 'Available Slots'],
    'Count': [total_slots, occupied_slots, available_slots]
}
df = pd.DataFrame(data)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
excel_filename = f'parking_occupancy_report_{timestamp}.xlsx'
df.to_excel(excel_filename, index=False)
print(f"Excel file created: {excel_filename}")

w, h = 400, 90
cv2.rectangle(frame_new, (0, 0), (w, h), (255, 0, 255), -1)
cv2.putText(frame_new, f"Total Slots: {total_slots}", (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(frame_new, f"Occupied (Red): {occupied_slots}", (10, 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(frame_new, f"Available: {available_slots}", (10, 90), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow('frame', frame_new)
cv2.waitKey(0)
cv2.destroyAllWindows()