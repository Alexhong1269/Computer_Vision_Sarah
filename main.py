import cv2
from core.hand_tracker import HandTracker

def main():
    tracker = HandTracker(detection_confidence=0.5)
    cap = cv2.VideoCapture(0) # 0 = default webcam
    cv2.namedWindow("Hand Tracker Test", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Hand Tracker Test", 100, 100)
    cv2.resizeWindow("Hand Tracker Test", 1280, 720)

    while True:
        success, frame = cap.read()

        if not success:
            break
        frame = cv2.flip(frame, 1) #mirror image
        results = tracker.process_frame(frame)
        frame = tracker.draw_landmarks(frame, results)

        cv2.imshow("Hand Tracker Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
        
