from PIL import Image
import os
import numpy as np
import cv2
import Brickoganize
import threading
import time
def capture_background(cap):
    ret, background = cap.read()
    if not ret:
        print("Error: Could not capture background.")
        exit()
    return cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

def detect_foreground(background, frame, threshold=40):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(background, gray_frame)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return thresh, (x, y, w, h)
    else:
        return thresh, (0, 0, 0, 0)
def color(frame, foreground_contour):
    # Detect the color of the brick in the frame
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define color ranges for LEGO bricks
    color_ranges = {
        #'black': ([0, 0, 0], [180, 255, 46], (0, 0, 0)),
        'white': ([0, 0, 221], [180, 30, 255], (255, 255, 255)),
        'red': ([0, 43, 46], [10, 255, 255], (0, 0, 255)),
        'orange': ([11, 43, 46], [25, 255, 255], (0, 165, 255)),
        'yellow': ([26, 43, 46], [34, 255, 255], (0, 255, 255)),
        'green': ([35, 43, 46], [77, 255, 255], (0, 255, 0)),
        'cyan': ([78, 43, 46], [99, 255, 255], (255, 255, 0)),
        'blue': ([100, 43, 46], [124, 255, 255], (255, 0, 0)),
        'purple': ([125, 43, 46], [125, 255, 255], (128, 0, 128)),
    }
    max_overlap_area = 0
    best_contour = None
    best_color_name = None
    best_screen = None

    for color_name, (lower, upper, screen) in color_ranges.items():
        lower = np.array(lower, np.uint8)
        upper = np.array(upper, np.uint8)
        mask = cv2.inRange(hsv, lower, upper)
        kernal = np.ones((5, 5), "uint8")
        cmask = cv2.dilate(mask, kernal)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                overlap_x1 = max(foreground_contour[0], x)
                overlap_y1 = max(foreground_contour[1], y)
                overlap_x2 = min(foreground_contour[0] + foreground_contour[2], x + w)
                overlap_y2 = min(foreground_contour[1] + foreground_contour[3], y + h)

                if overlap_x1 < overlap_x2 and overlap_y1 < overlap_y2:  # Valid overlap
                    overlap_area = (overlap_x2 - overlap_x1) * (overlap_y2 - overlap_y1)
                    if overlap_area > max_overlap_area:
                        max_overlap_area = overlap_area
                        best_contour = (x, y, w, h)
                        best_color_name = color_name
                        best_screen = screen

    if best_contour:
        x, y, w, h = best_contour
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), best_screen, 2)
        cv2.putText(frame, best_color_name, (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, best_screen)


    

def main():
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # Open webcam

    print("Capturing background...")
    time.sleep(1.5) 
    background = capture_background(cap)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        foreground_mask,contour = detect_foreground(background, frame)
        
        if np.count_nonzero(foreground_mask) > 700:
            print("LEGO detected!")
            cv2.imwrite('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/'+"test.jpg", frame)
            print("save image successfuly!")
            print("-------------------------")

            threading.Thread(target=Brickoganize.get_brickognize_data, args=('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/test.jpg',)).start()
        else:
            print("No LEGO detected.")
        
        cv2.imshow("Foreground Mask", foreground_mask)
        cv2.imshow("Frame", frame)
        # Display the frame
        
        x, y, w, h = contour
        color(frame,contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Contour", (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
        cv2.imshow("Foreground Mask", foreground_mask)
        
        cv2.imshow("Frame", frame)
        time.sleep(0.25)  # Add a small delay to control the frame rate
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

'''
if __name__ == '__main__':
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture background image")
        cap.release()
        cv2.destroyAllWindows()
        exit()
    cv2.imwrite('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/'+"background.jpg", frame)
    background=Image.open('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/'+"background.jpg")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/'+"current.jpg", frame)
        current_frame=Image.open('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/'+"current.jpg")
        difference = compare(background, current_frame)
        if index <= 10:
            if index == 1:
                threshold = difference
            else:
                threshold =max(threshold,difference)
                index += 1
        threshold*=1.3
        cv2.waitKey(200)
        print(difference)

        if difference > threshold:
            print(True)
        else:
            print(False)
        
        cv2.imshow('Frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
'''