import cv2
import cv2.aruco as aruco
import numpy as np

#This function calculates the center and orientation of a single marker.
def find_marker_center_and_orientation(corners):         
    c = corners.reshape((4, 2))
    c_sum = np.sum(c, axis=0)
    center = (c_sum / 4).astype(int)
    vector = c[0] - c[2]
    angle = np.arctan2(vector[1], vector[0])
    orientation = np.degrees(angle) % 360
    return center, orientation

#Detects ArUco markers in the provided frame and returns their center positions and orientations.
def find_markers(frame, aruco_dict, aruco_params):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    # print(f"Corners: {corners}")  # Debugging
    # print(f"IDs: {ids}")

    marker_info = {}
    if ids is not None:
        ids = ids.flatten()  # Flatten the ids array to ensure proper shape
        for i, corner_group in enumerate(corners):
            marker_id = ids[i]
            center, orientation = find_marker_center_and_orientation(corner_group)
            marker_info[marker_id] = {'center': center, 'orientation': orientation}

            # Draw individual marker
            aruco.drawDetectedMarkers(frame, [corner_group], np.array([marker_id]).reshape(-1, 1))
    return marker_info


def draw_lines(frame, marker_info):
    """
    Draw lines between markers to create a path and a quadrilateral.
    """
    # Drawing the paths for bot (7), pallet (8), and destination (9) markers
    for marker_id, color in [(7, (0, 255, 255)), (8, (255, 255, 0)), (9, (255, 0, 255))]:
        if marker_id in marker_info:
            pos = tuple(marker_info[marker_id]['center'])
            cv2.circle(frame, pos, 5, color, -1)  # Draw a small circle at the marker position

    # Drawing the quadrilateral for markers 10, 11, 12, and 13
    quad_ids = [10, 11, 12, 13]
    if all(marker_id in marker_info for marker_id in quad_ids):
        quad_points = [tuple(marker_info[marker_id]['center']) for marker_id in quad_ids]
        quad_points.append(quad_points[0])  # Close the loop
        for i in range(4):  # There are 4 lines in a quadrilateral
            cv2.line(frame, quad_points[i], quad_points[i+1], (0, 255, 0), 2)

    # Drawing the line from marker 7 to 8
    if 7 in marker_info and 8 in marker_info:
        start_pos_7_8 = tuple(marker_info[7]['center'])
        end_pos_7_8 = tuple(marker_info[8]['center'])
        cv2.line(frame, start_pos_7_8, end_pos_7_8, (0, 255, 255), 2)

    # Drawing the line from marker 8 to 9
    if 8 in marker_info and 9 in marker_info:
        start_pos_8_9 = tuple(marker_info[8]['center'])
        end_pos_8_9 = tuple(marker_info[9]['center'])
        cv2.line(frame, start_pos_8_9, end_pos_8_9, (255, 0, 255), 2)

    return frame  # Make sure to return the modified frame if this function is not modifying the frame in place