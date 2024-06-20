import cv2
import numpy as np
import math

# Step 2: Configure the desired width and height
desired_width = 640  # Set the desired width
desired_height = 480  # Set the desired height
dim = (desired_width, desired_height)

# Step 8: Compute the center of the ROI
roi_center_x = (480 - 240) // 2

# Function to calculate the angle between two lines
def calculate_angle(line):
    x1, y1, x2, y2 = line
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return angle

# Open the default camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    
    # Resize the frame
    resized_image = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    
    # Step 3: Define ROI
    roi = resized_image[150:, 240:480]
    
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Step 6: Noise reduction (optional, experiment with parameters)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian blur
    
    kernel = np.ones((7, 7), np.uint8)
    ed = cv2.erode(gray, kernel, iterations=1)  # Use erosion to remove small noise
    ed = cv2.dilate(ed, kernel, iterations=1)  # Use dilation to close gaps
    
    edges = cv2.Canny(ed, 50, 150, apertureSize=3)
    
    # Step 7: Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    
    # Step 9: Draw lines on the original image (only within the ROI) and compute deviations and angles
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Compute the midpoint of the line
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            # Calculate the deviation from the center of the ROI
            deviation = mid_x - roi_center_x
            # Calculate the angle of the detected line
            angle = calculate_angle((x1, y1, x2, y2))
            # Calculate the angle difference from the vertical reference line (90 degrees)
            angle_diff = abs(90 - abs(angle))
            # Draw the line on the resized image
            cv2.line(resized_image, (x1 + 240, y1 + 150), (x2 + 240, y2 + 150), (0, 255, 0), 2)
            # Draw the midpoint and the deviation line
            cv2.circle(resized_image, (mid_x + 240, mid_y + 150), 5, (255, 0, 0), -1)
            cv2.line(resized_image, (roi_center_x + 240, mid_y + 150), (mid_x + 240, mid_y + 150), (0, 0, 255), 1)
            # Display the angle difference with black text
            cv2.putText(resized_image, f"Angle: {angle_diff:.2f}", (mid_x + 240, mid_y + 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Draw the center line of the ROI
    cv2.line(resized_image, (roi_center_x + 240, 150), (roi_center_x + 240, 150 + roi.shape[0]), (255, 255, 0), 2)
    
    # Step 10: Display the result
    cv2.imshow("Detected Lines and Angles", resized_image)
    
    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
