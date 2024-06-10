import cv2
import numpy as np

# Step 1: Read the image
image_path = "02.jpg"
image = cv2.imread(image_path)

# Step 2: Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 3: Edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Step 4: Hough Line Transform
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

# Step 5: Draw lines on the image
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Step 6: Display the result
cv2.imshow("Detected Lines", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
