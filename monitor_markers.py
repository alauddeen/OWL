import cv2
import cv2.aruco as aruco
import numpy as np
import time
from video import find_markers
import tkinter as tk

# Configuration
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
aruco_params = aruco.DetectorParameters()

def update_marker_positions(marker_info, marker_ids, text_widgets):
    for marker_id in marker_ids:
        text = f"Marker {marker_id}: Not detected"
        if marker_id in marker_info:
            text = f"Marker {marker_id}: {marker_info[marker_id]['center']}"
        text_widgets[marker_id].set(text)

def main():
    # Setup the tkinter window
    root = tk.Tk()
    root.title("Marker Positions")

    # Create text variables for each marker
    text_vars = {marker_id: tk.StringVar() for marker_id in range(7, 10)}
    for marker_id, text_var in text_vars.items():
        text_var.set(f"Marker {marker_id}: Awaiting detection")
        tk.Label(root, textvariable=text_var).pack()

    cap = cv2.VideoCapture(0)
    start_time = [time.time()]  # Use a mutable object like a list to store the start time

    def task():
        nonlocal start_time  # Declare nonlocal to modify the start time outside of this function
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            root.after(1000, task)  # Try again after 1 second
            return

        marker_info = find_markers(frame, aruco_dict, aruco_params)
        
        # # Update corner markers once at the start
        # if time.time() - start_time[0] < 1:  # Only at the first second
        #     update_marker_positions(marker_info, range(10, 14), text_vars)

        # Update positions of markers 7, 8, and 9 every 5 seconds
        if time.time() - start_time[0] >= 5:
            update_marker_positions(marker_info, range(7, 10), text_vars)
            start_time[0] = time.time()  # Reset the timer

        root.after(1000, task)  # Rerun the task every 1 second for updates

    task()
    root.mainloop()  # Start the tkinter event loop

    cap.release()

if __name__ == '__main__':
    main()
