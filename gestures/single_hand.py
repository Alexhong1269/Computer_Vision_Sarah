class SingleHandGestures:
    FINGER_TIPS = {
        "thumb" : 4,
        "index" : 8,
        "middle" : 12,
        "ring" : 16,
        "pinky" : 20,
    }
    FINGER_JOINTS = {
        "thumb" : 2,
        "index" : 6,
        "middle" : 10,
        "ring" : 14,
        "pinky" : 18
    }
    WRIST = 0

    @staticmethod
    def _distance_from_wrist(landmark, wrist):
        return ((landmark.x - wrist.x) ** 2 + (landmark.y - wrist.y) ** 2) ** .05

    #checking to see if the distance of the tip to wrist is larger meaning finger is extended
    def _is_finger_extended(self, hand_landmarks, finger_name):
        wrist = hand_landmarks.landmark[self.WRIST]
        tip = hand_landmarks.landmark[self.FINGER_TIPS[finger_name]]
        joint = hand_landmarks.landmark[self.FINGER_JOINTS[finger_name]]

        tip_distance = self._distance_from_wrist(tip, wrist)
        joint_distance = self._distance_from_wrist(joint, wrist)

        return tip_distance > joint_distance

    def get_finger_states(self, hand_landmarks):
        #gives us a list of the finger state
        return {
            finger: self._is_finger_extended(hand_landmarks, finger)
            for finger in self.FINGER_TIPS
        }