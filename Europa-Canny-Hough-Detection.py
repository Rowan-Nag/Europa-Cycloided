import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

def drawLines(lines, img):
    
    if lines is None:
        return img
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr[0], arr[1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*r
        y0 = b*r
        x1 = int(x0 + 100*(-b))
        y1 = int(y0 + 100*(a))
        x2 = int(x0 - 100*(-b))
        y2 = int(y0 - 100*(a))
        cv.line(img, (x1, y1), (x2, y2), (255), 2)
    return img

def preprocess_image(image):
    # Convert to grayscale
    image = cv.resize(image, (200, 200))
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return image

def process(image):
    image = cv.GaussianBlur(image, (5, 5), 0)
    return image

def canny(image, thresh1, thresh2):
    edges = cv.Canny(image, thresh1, thresh2)
    return edges

def houghLines(image, rho, theta, threshold):
    lines = cv.HoughLines(image, rho=rho, theta=theta, threshold=threshold)

    return drawLines(lines, preprocessed_img.copy())

def houghLinesP(image, rho, theta, threshold):
    lines = cv.HoughLinesP(image, rho=rho, theta=theta, threshold=threshold, minLineLength=30, maxLineGap=5)

    return drawLines(lines, preprocessed_img.copy())



def on_trackbar(val):
    threshold1 = cv.getTrackbarPos('Threshold1', 'Controls')
    threshold2 = cv.getTrackbarPos('Threshold2', 'Controls')
    houghThreshold = cv.getTrackbarPos('Hough Threshold', 'Controls')
    houghTheta = cv.getTrackbarPos('Hough Theta', 'Controls') * np.pi/180
    houghRho = cv.getTrackbarPos('Hough Rho', 'Controls') / 20

    processed_img = process(preprocessed_img)
    edges = canny(processed_img, threshold1, threshold2)
    hough = houghLines(edges, houghRho, houghTheta, houghThreshold)
    houghP = houghLinesP(edges, houghRho, houghTheta, houghThreshold)
    combined = np.vstack((
        np.hstack((processed_img, edges)),
        np.hstack((hough, houghP))
        ))
    cv.imshow('Canny Edge Detection', combined)

# Main script

image_path = Path().resolve() / 'data' / 'C0374649039R_full.jpg'
orig_img = cv.imread(image_path)
preprocessed_img = preprocess_image(orig_img)

# preprocessed_img = cv.convertScaleAbs(preprocessed_img)


cv.namedWindow('Canny Edge Detection')
cv.moveWindow('Canny Edge Detection', 0, 100)

cv.namedWindow("Controls")
cv.moveWindow("Controls", 0, 0) 

# Create trackbars for threshold adjustment
cv.createTrackbar('Threshold1', 'Controls', 200, 600, on_trackbar)
cv.createTrackbar('Threshold2', 'Controls', 600, 1000, on_trackbar)
cv.createTrackbar('Hough Threshold', 'Controls', 70, 200, on_trackbar)
cv.createTrackbar('Hough Theta', 'Controls', 0, 4, on_trackbar)
cv.createTrackbar('Hough Rho', 'Controls', 1, 20, on_trackbar)
# Initial call to display the image
on_trackbar(0)

# Wait until user exits the program
cv.waitKey(0)
cv.destroyAllWindows()