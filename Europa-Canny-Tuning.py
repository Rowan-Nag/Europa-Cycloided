import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

def preprocess_image(image):
    # Convert to grayscale
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    # image = cv.dilate(image, kernel, iterations=1)
    # image = cv.erode(image, kernel, iterations=1)
    image = cv.GaussianBlur(image, (5, 5), 0)
    # Apply adaptive histogram equalization to enhance contrast
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    image = clahe.apply(image)
    # Directional filtering (using Sobel filters)
    # sobelx = cv.Sobel(image, cv.CV_64F, 1, 0, ksize=5)
    # sobely = cv.Sobel(image, cv.CV_64F, 0, 1, ksize=5)
    # directional_filtered = cv.magnitude(sobelx, sobely)
    
    # # Local variance analysis
    # image = cv.Laplacian(directional_filtered, cv.CV_64F)
    
    return image


def process(image):

    # sharpen = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    # unsharp_mask = np.array([[1, 4, 6, 4, 1],
    #                     [4, 16, 24, 16, 4],
    #                     [6, 24, -476, 24, 6],
    #                     [4, 16, 24, 16, 4],
    #                     [1, 4, 6, 4, 1]]) / -256
                        
    # image = cv.filter2D(image, -1, unsharp_mask)
    # image = cv.filter2D(image, -1, unsharp_mask)
    # image = cv.filter2D(image, -1, unsharp_mask)
    # image = cv.GaussianBlur(image, (3, 3), 0)
    return image

def houghLines(image):
    lines = cv.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=50, minLineLength=30, maxLineGap=5)

    # Draw detected lines
    output = grayscale.copy()
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(output, (x1, y1), (x2, y2), (255), 2)
    return output

def on_trackbar(val):
    threshold1 = cv.getTrackbarPos('Threshold1', 'Controls')
    threshold2 = cv.getTrackbarPos('Threshold2', 'Controls')
    
    ridges = process(preprocessed_img)
        
    edges = cv.Canny(ridges, threshold1, threshold2)
    hough = houghLines(edges)
    combined = np.vstack((
        np.hstack((hough, edges)),
        np.hstack((grayscale, preprocessed_img))
        ))
    cv.imshow('Canny Edge Detection', combined)

# Main script
image_path = Path().resolve() / 'data' / 'C0374649039R_full.jpg'  # Replace with your image path
orig_img = cv.imread(image_path)
orig_img = cv.resize(orig_img, (500, 500))
grayscale = cv.cvtColor(orig_img, cv.COLOR_BGR2GRAY)
# Pre-processing
preprocessed_img = preprocess_image(orig_img)

# Convert to 8-bit unsigned integer type
preprocessed_img = cv.convertScaleAbs(preprocessed_img)


cv.namedWindow('Canny Edge Detection')
cv.moveWindow('Canny Edge Detection', 0, 100)

cv.namedWindow("Controls")
cv.moveWindow("Controls", 0, 0) 

# Create trackbars for threshold adjustment
cv.createTrackbar('Threshold1', 'Controls', 200, 600, on_trackbar)
cv.createTrackbar('Threshold2', 'Controls', 600, 1000, on_trackbar)

# Initial call to display the image
on_trackbar(0)

# Wait until user exits the program
cv.waitKey(0)
cv.destroyAllWindows()