import cv2
import mediapipe as mp

class HandTracker:
    #max_hands capped at 2 to make the heart
    #.7 to avoid false positives
    def __init__(self, max_hands = 2, detection_confidence = 0.7, tracking_confidence = 0.5):
        #media pipeline prebuilt hand tracking
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands = max_hands,
            min_detection_confidence = detection_confidence,
            min_tracking_confidence = tracking_confidence
        )
        #to draw points to see the hand
        self.mp_drawing = mp.solutions.drawing_utils

    #frame processing
    def process_frame(self, frame):
        #MediaPipe wants RFB images, but OpenCV gices us BGR
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results

    #drawing landmarks to make sure its working
    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    