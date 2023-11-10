import cv2
from video import find_markers, draw_lines
from pathplanning import generate_path_commands
from robotcom import send_command_to_node_mcu
import cv2.aruco as aruco
import numpy as np

NODEMCU_BASE_URL = 'http://192.168.162.102'

# Define the ArUco dictionary you want to use
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
# Define the detector parameters
aruco_params = aruco.DetectorParameters()

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)  # Adjust the device index according to your setup

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break
           
            # Process frame for markers
            marker_info = find_markers(frame, aruco_dict,aruco_params)

            # Generate path commands based on marker info
            commands = generate_path_commands(marker_info)

            # Send commands to NodeMCU
            for command in commands:
                send_command_to_node_mcu(NODEMCU_BASE_URL, command)

            # Display the resulting frame with lines drawn
            draw_lines(frame, marker_info)
            cv2.imshow('Detected Markers & Paths', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
