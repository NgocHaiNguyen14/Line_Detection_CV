import cv2
import numpy as np
#This is program detected the line successfully, next , we need to have process the output ...
# ... and calculate the deviation / steering angle


image_path = "actual_img05.jpg"
image = cv2.imread(image_path)
desired_width = 640  
desired_height = 480 
dim = (desired_width, desired_height)
resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
roi = resized_image[150:,240:480]

gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)  

kernel = np.ones((7, 7), np.uint8)
ed = cv2.erode(gray, kernel, iterations=1)  # Use erosion to remove small noise
ed = cv2.dilate(gray, kernel, iterations=1)  # Use dilation to close gaps

edges = cv2.Canny(ed, 50, 150, apertureSize=3)
# Step 7: Hough Line Transform
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

# Step 8: Draw lines on the original image (only within the ROI)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(resized_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Step 9: Display the result
cv2.imshow("Detected Lines", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
