import cv2
import numpy as np

def show_wait_destroy(winname, img):
    cv2.imshow(winname, img)
    cv2.moveWindow(winname, 500, 0)
    cv2.waitKey(0)
    cv2.destroyWindow(winname)

def get_hor(horizontal):
    cols = horizontal.shape[1]
    horizontal_size = cols // 30
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    return horizontal

def get_ver(vertical):
    rows = vertical.shape[0]
    verticalsize = rows // 30
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)
    
    return vertical
    
def remove_trash(horizontal, vertical):
    horizontal = horizontal.copy()
    lines = cv2.HoughLinesP(vertical, 1, np.pi/180,  50)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y1 - y2) > 20:
            cv2.line(horizontal, (x1, y1), (x2, y2), (255), 1)
    return horizontal

def remove_trash_ver(vertical):
    blank_image = np.zeros(vertical.shape, np.uint8)
    lines = cv2.HoughLinesP(vertical, 1, np.pi/180,  50)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y1 - y2) > 20:
            cv2.line(blank_image, (x1, y1), (x2, y2), (255), 1)
    return blank_image

def combine_two_image(horizontal, vertical):
    horizontal = horizontal.copy()
    lines = cv2.HoughLinesP(vertical, 1, np.pi/180,  50)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(horizontal, (x1, y1), (x2, y2), (255), 1)
    return horizontal

def remove_text(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                            cv2.THRESH_BINARY, 15, -2)

    horizontal = np.copy(bw)
    vertical = np.copy(bw)

    horizontal = get_hor(horizontal)
    vertical = remove_trash_ver(get_ver(vertical))

    result = remove_trash(horizontal, vertical)
    return horizontal, vertical, result, img

def draw_fulline(image):
    image = image.copy()
    width, height = image.shape
    blank_image = np.zeros(image.shape, np.uint8)

    lines = cv2.HoughLinesP(image, 1, np.pi/180,  50)

    for line in lines:
        x1, y1, x2, y2 = line[0]

        if y1 == y2:
            cv2.line(blank_image,(0,y1), (height,y2), (255),1)
        elif (x1  == x2):
            cv2.line(blank_image,(x1,0), (x2,width), (255), 1)
    return blank_image

