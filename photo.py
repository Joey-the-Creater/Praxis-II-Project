import cv2
import Brickoganize

if __name__ == "__main__":
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("frame", frame)
        k=cv2.waitKey(1)
        if k == ord('s'): 
            cv2.imwrite('c:/Users/swale/Desktop/UofT/Year 1/ESC102/Image/'+"test.jpg", frame)
            print("save image successfuly!")
            print("-------------------------")
            Brickoganize.get_brickognize_data('c:/Users/swale/Desktop/UofT/Year 1/ESC102/Image/test.jpg')
        elif k== ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()