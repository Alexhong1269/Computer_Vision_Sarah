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
    #help with 
    def _distance(landmark_a, landmark_b):
        return ((landmark_a.x - landmark_b. x) ** 2 + (landmark_a.y - landmark_b.y) ** 2) ** 0.5
    
    #thumb checker
    def _is_thumb_extended(self, hand_landmarks):
        thumb_tip = hand_landmarks.landmark[4]
        thumb_mcp = hand_landmarks.landmark[2]
        index_mcp = hand_landmarks.landmark[5]

        tip_to_index = self._distance(thumb_tip, index_mcp)
        base_to_index = self._distance(thumb_mcp, index_mcp)

        #return
        return tip_to_index > base_to_index * 1.3


    #checking to see if the distance of the tip to wrist is larger meaning finger is extended
    def _is_finger_extended(self, hand_landmarks, finger_name):
        wrist = hand_landmarks.landmark[self.WRIST]
        tip = hand_landmarks.landmark[self.FINGER_TIPS[finger_name]]
        joint = hand_landmarks.landmark[self.FINGER_JOINTS[finger_name]]

        tip_distance = self._distance(tip, wrist)
        joint_distance = self._distance(joint, wrist)

        return tip_distance > joint_distance

    def get_finger_states(self, hand_landmarks):
        states = {}

        for finger in self.FINGER_TIPS:
            if finger == "thumb":
                states[finger] = self._is_thumb_extended(hand_landmarks)
            else:
                states[finger] = self._is_finger_extended(hand_landmarks, finger)
        return states
    
    #gesture matching
    def is_fist(self, hand_landmarks):
        states = self.get_finger_states(hand_landmarks)
        return not any(states.values())
    
    def is_open_palm(self, hand_landmarks):
        states = self.get_finger_states(hand_landmarks)
        return all(states.values())

    def is_thumb_up(self, hand_landmarks):
        states = self.get_finger_states(hand_landmarks)
        return states["thumb"] and not any(
            states[f] for f in ["index", "middle", "ring", "pinky"]
        )

    def is_peace_sign(self, hand_landmarks):
        states = self.get_finger_states(hand_landmarks)
        return states["index"] and states["middle"] and not any(
            states[f] for f in ["ring", "pinky"]
        )
    
    def is_pointing(self, hand_landmarks):
        states = self.get_finger_states(hand_landmarks)
        return states["index"] and not any(
            states[f] for f in ["middle", "ring", "pinky"]
        )

    #method to detect the action
    def detect_gesture(self, hand_landmarks):
        if self.is_fist(hand_landmarks):
            return "Fist"
        if self.is_open_palm(hand_landmarks):
            return "Open Palm"
        if self.is_thumb_up(hand_landmarks):
            return "Thumbs up"
        if self.is_peace_sign(hand_landmarks):
            return "Peace Sign"
        if self.is_pointing(hand_landmarks):
            return "Pointing"
        #return
        return None
    