import cv2
import sys
import numpy as np
from glob import glob

# Stage 1: reading, averaging, and blurring images
def Stage_1(dir_path):
    print("Stage 1: reading, averaging, and blurring images")
    dir_path += '/*.jpg'
    dir_data = glob(dir_path)
    avg_image = np.zeros((500, 500), dtype=float)  
    for img in dir_data:
        image = cv2.imread(img)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (500, 500))   
        image = cv2.GaussianBlur(image, (77, 77), 0)
        image_arr = np.array(image, dtype=float)
        avg_image += (image_arr/len(dir_data))
    avg_image = np.array(np.round(avg_image), dtype=np.uint8)
    cv2.imwrite('Stage_1.jpg', avg_image)
    return avg_image, dir_data

# Stage 2: thresholding darkest parts
def Stage_2(avg_image):
    print("Stage 2: thresholding darkest parts")
    threshold_image = cv2.adaptiveThreshold(avg_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 2)
    threshold_image = avg_image > threshold_image
    threshold_image = threshold_image.astype(np.uint8)*255  # converts from bool/binary to int out of 255
    cv2.imwrite('Stage_2.jpg', threshold_image)
    return threshold_image

# Stage 3: edge detection
def Stage_3(threshold_image):
    print("Stage 3: edge detection")
    edge_image = cv2.Canny(threshold_image, 100, 200)
    cv2.imwrite("Stage_3.jpg", edge_image)
    return edge_image

# Stage 4: drawing contours on original image
def Stage_4(edge_image, dir_data):
    print("Stage 4: drawing contours on original image")
    (contours,_) = cv2.findContours(edge_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    org_image = cv2.imread(dir_data[0])
    org_image = cv2.resize(org_image, (500, 500))
    contours_image = cv2.drawContours(org_image, contours, -1000, (0, 255, 0), 1)
    cv2.imwrite("Stage_4.jpg", contours_image)
    return contours_image

def Smear_Detector(dir_path):
    avg_image, dir_data = Stage_1(dir_path)
    threshold_image = Stage_2(avg_image)
    edge_image = Stage_3(threshold_image)
    contours_image = Stage_4(edge_image, dir_data)
    cv2.imshow("Final Output (Stage 4)", contours_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect image folder path.")
        sys.exit(1)
    Smear_Detector(sys.argv[1])