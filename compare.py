from PIL import Image, ImageTk
import sys
import os
import numpy as np
import cv2
import Brickoganize
import threading
import time
import tkinter as tk
from tkinter import messagebox

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
        with open('Image/color.txt', 'w') as f:
            f.write(best_color_name)
        f.close()


    

def main(root):
    def check_status():
        with open("Status.txt", "r") as file:
            status = file.read().strip()
        return status

    def update_frame():
        status = check_status()
        if status == "Status: Start":
            ret, frame = cap.read()
            if not ret:
                cap.release()
                cv2.destroyAllWindows()
                return

            foreground_mask, contour = detect_foreground(background, frame)

            if np.count_nonzero(foreground_mask) > 700:
                #print("LEGO detected!")
                cv2.imwrite('Image/' + "test.jpg", frame)
                #print("Save image successfully!")
                #print("-------------------------")

                threading.Thread(target=Brickoganize.get_brickognize_data,
                                 args=('Image/test.jpg',)).start()
            else:
                #print("No LEGO detected.")
                with open('Image/response.txt', 'w') as f:
                    f.write("LEGO not detected")
                f.close()
            x, y, w, h = contour
            color(frame, contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Contour", (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
            frame = cv2.resize(frame, (400, 300))
            # Convert the frame to an image format compatible with Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update the label with the new frame
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

        else:
            # Create a black screen
            black_screen = np.zeros((300, 400, 3), dtype=np.uint8)
            black_screen_rgb = cv2.cvtColor(black_screen, cv2.COLOR_BGR2RGB)
            cv2.putText(black_screen_rgb, "No Video Feed", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            img = Image.fromarray(black_screen_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            # Display the black screen
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

        # Schedule the next frame update
        root.after(250, update_frame)

    print("Initializing...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Open webcam

    print("Capturing background...")
    time.sleep(1.5)
    background = capture_background(cap)

    # Create a frame to hold the video feed and buttons
    main_frame = tk.Frame(root, width=400, height=300)
    main_frame.pack(side=tk.RIGHT, padx=20, pady=20)
    main_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content

    # Create a label to display the video feed
    video_label = tk.Label(main_frame)
    video_label.pack()

    # Start updating frames
    update_frame()

    # Handle window close event
    def on_closing():
        cap.release()
        cv2.destroyAllWindows()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

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