import cv2
from core.hand_tracker import HandTracker
from gestures.single_hand import SingleHandGestures
from gestures.heart import HeartGesture
from core.state_manager import GestureStateManager

def main():
    gesture_detector = SingleHandGestures()
    heart_detector = HeartGesture()
    state_manager = GestureStateManager(debounce_frames=5)

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

        if results.multi_hand_landmarks:
            is_heart = False
            if len(results.multi_hand_landmarks) == 2:
                is_heart = heart_detector.is_heart_gesture(
                    results.multi_hand_landmarks, results.multi_handedness
                )
            if is_heart:
                cv2.putText(
                    frame, "Heart <3", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3
                )
        
            else:
                for hand_landmarks in results.multi_hand_landmarks:
                    raw_gesture = gesture_detector.detect_gesture(hand_landmarks)
                    confirmed = state_manager.update(raw_gesture)
                    if confirmed:
                        cv2.putText(
                            frame, confirmed, (50,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3
                        )



        cv2.imshow("Hand Tracker Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()