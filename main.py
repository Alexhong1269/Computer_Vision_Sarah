import cv2
from core.hand_tracker import HandTracker
from gestures.single_hand import SingleHandGestures

def main():
    tracker = HandTracker(detection_confidence=0.5)
    cap = cv2.VideoCapture(0) # 0 = default webcam
    cv2.namedWindow("Hand Tracker Test", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Hand Tracker Test", 100, 100)
    cv2.resizeWindow("Hand Tracker Test", 1280, 720)

    while True:
        success, frame = cap.read()
        gesture_detector = SingleHandGestures()

        if not success:
            break
        frame = cv2.flip(frame, 1) #mirror image
        results = tracker.process_frame(frame)
        frame = tracker.draw_landmarks(frame, results)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture = gesture_detector.detect_gesture(hand_landmarks)
                if gesture:
                    cv2.putText(
                        frame, gesture(50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3
                    )

        cv2.imshow("Hand Tracker Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
        
