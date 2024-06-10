import cv2
import numpy as np

# Step 1: Read the image
image_path = "03.jpg"
image = cv2.imread(image_path)

# Step 2: Configure the desired width and height
desired_width = 640  # Set the desired width
desired_height = 480  # Set the desired height
dim = (desired_width, desired_height)

# Step 3: Resize the image
resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Step 4: Convert to grayscale
gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Step 5: Edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Step 6: Hough Line Transform
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

# Step 7: Draw lines on the image
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(resized_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Step 8: Display the result
cv2.imshow("Detected Lines", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
