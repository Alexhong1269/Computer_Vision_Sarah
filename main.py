import cv2
import random
from core.hand_tracker import HandTracker
from gestures.single_hand import SingleHandGestures
from gestures.heart import HeartGesture
from core.state_manager import GestureStateManager
from effects.particles import ParticleSystem

CONFETTI_COLORS = [
    (0,0,255), (0, 255, 0), (255,0, 0),
    (0, 255, 255), (255, 0, 255), (255, 255, 0)
]

LASER_COLOR = (0, 0, 255)
HEART_COLOR = (147, 20, 255)

def main():
    gesture_detector = SingleHandGestures()
    heart_detector = HeartGesture()
    particle_system = ParticleSystem()
    state_manager = GestureStateManager(debounce_frames=5, cooldown_seconds=1.0)
    heart_state_manager = GestureStateManager(debounce_frames=5, cooldown_seconds=1.0)

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

        frame_height, frame_width = frame.shape[0], frame.shape[1]

        if results.multi_hand_landmarks:
            is_heart = False
            if len(results.multi_hand_landmarks) == 2:
                is_heart = heart_detector.is_heart_gesture(
                    results.multi_hand_landmarks, results.multi_handedness
                )
            if is_heart:
                confirmed_heart = heart_state_manager.update("heart")

                hands = heart_detector._get_hands_by_label(
                    results.multi_hand_landmarks, results.multi_handedness
                )
                left_wrist = hands["Left"].landmark[0]
                right_wrist = hands["Right"].landmark[0]

                mid_x = int(((left_wrist.x + right_wrist.x) / 2) * frame_width)
                mid_y = int(((left_wrist.y + right_wrist.y) / 2) * frame_height)

                if confirmed_heart and heart_state_manager.can_trigger():
                    particle_system.emit(mid_x,mid_y, HEART_COLOR, count=40)
                    heart_state_manager.trigger()
                cv2.putText(
                    frame, "Heart <3", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3
                )
        
            else:
                heart_state_manager.update(None)

                for hand_landmarks in results.multi_hand_landmarks:
                    raw_gesture = gesture_detector.detect_gesture(hand_landmarks)
                    confirmed = state_manager.update(raw_gesture)

                    wrist = hand_landmarks.landmark[0]
                    x = int(wrist.x * frame_width)
                    y = int(wrist.y * frame_height)
                    
                    if confirmed == "Fist" and state_manager.can_trigger():
                        particle_system.emit_laser_burst(x, y)
                        state_manager.trigger()
                    elif confirmed == "Peace Sign" and state_manager.can_trigger():
                        color = random.choice(CONFETTI_COLORS)
                        particle_system.emit(x, y, color, count=40)
                        state_manager.trigger()

                    if confirmed:
                        cv2.putText(
                            frame, confirmed, (50,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3
                        )

        particle_system.update()
        particle_system.draw(frame)
        
        cv2.imshow("Hand Tracker Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()