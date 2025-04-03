import numpy as np
import cv2

# turn on cam
webcam = cv2.VideoCapture(0)

# Define color ranges and corresponding labels
colors = [
    {"lower": np.array([136, 87, 111], np.uint8), "upper": np.array([180, 255, 255], np.uint8), "label": "Red Colour", "color": (0, 0, 255)},
    {"lower": np.array([25, 52, 72], np.uint8), "upper": np.array([102, 255, 255], np.uint8), "label": "Green Colour", "color": (0, 255, 0)},
    {"lower": np.array([94, 80, 2], np.uint8), "upper": np.array([120, 255, 255], np.uint8), "label": "Blue Colour", "color": (255, 0, 0)},
]

while (1):
    _, imageFrame = webcam.read()

    # Convert BGR to HSV colorspace
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Kernel for dilation
    kernal = np.ones((5, 5), "uint8")

    for color in colors:
        # Create mask for the color
        mask = cv2.inRange(hsvFrame, color["lower"], color["upper"])
        mask = cv2.dilate(mask, kernal)
        res = cv2.bitwise_and(imageFrame, imageFrame, mask=mask)

        # Find contours for the color
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), color["color"], 2)
                cv2.putText(imageFrame, color["label"], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color["color"])

    # Display the result
    cv2.imshow("Color Detection", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
