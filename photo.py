import cv2
import Brickoganize
from PIL import Image
import numpy as np
def compare(img1: Image.Image, img2: Image.Image) -> int:
    gimg1 = cv2.cvtColor(np.array(img1), cv2.COLOR_BGR2GRAY)
    gimg2 = cv2.cvtColor(np.array(img2), cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gimg1, gimg2)
    return np.sum(diff)

    
if __name__ == "__main__":
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("frame", frame)
        k=cv2.waitKey(1)
        cv2.imwrite('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/'+"background.jpg", frame)
        if k == ord('s'): 
            cv2.imwrite('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/'+"test.jpg", frame)
            print("save image successfuly!")
            print("-------------------------")
            Brickoganize.get_brickognize_data('c:/Users/swale/Desktop/UofT/Year 1/Praxis-II-Project/Image/test.jpg')
        elif k== ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()