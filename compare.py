from PIL import Image
import os
import numpy as np
import cv2
import Brickoganize

def compare(img1: Image.Image, img2: Image.Image) -> int:
    gimg1 = cv2.cvtColor(np.array(img1), cv2.COLOR_BGR2GRAY)
    gimg2 = cv2.cvtColor(np.array(img2), cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gimg1, gimg2)
    return np.sum(diff)
index=1
import cv2
import numpy as np

def capture_background(cap):
    ret, background = cap.read()
    if not ret:
        print("Error: Could not capture background.")
        exit()
    return cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

def detect_foreground(background, frame, threshold=30):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(background, gray_frame)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    return thresh

def main():
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # Open webcam

    print("Capturing background...")
    background = capture_background(cap)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        foreground_mask = detect_foreground(background, frame)
        
        # Check if significant change is detected
        if np.count_nonzero(foreground_mask) > 500:
            print("LEGO detected!")
            cv2.imwrite('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/'+"test.jpg", frame)
            print("save image successfuly!")
            print("-------------------------")
            Brickoganize.get_brickognize_data('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/test.jpg')
        else:
            print("No LEGO detected.")
        
        # Display the result
        cv2.imshow("Foreground Mask", foreground_mask)
        cv2.imshow("Frame", frame)
        
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