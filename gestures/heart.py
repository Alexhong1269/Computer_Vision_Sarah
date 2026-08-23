class HeartGesture:
    THUMB_TIP = 4
    INDEX_TIP = 8

    @staticmethod
    #euclidian distance
    def _distance(landmark_a, landmark_b):
        return ((landmark_a.x - landmark_b.x) ** 2 + (landmark_a.y - landmark_b.y) ** 2) * .5
    
    def _get_hands_by_label(self, multi_hand_landmarks, multi_handedness):
        hands = {}
        #iterate through the hand landmarks to label left and right
        for landmarks, handedness in zip(multi_hand_landmarks, multi_handedness):
            #labeling
            label = handedness.classification[0].label
            hands[label] = landmarks
        return hands
    
    def is_heart_gesture(self, multi_hand_landmarks, multi_handedness, threshold=0.1):
        #checks if there are two hands by multiple landmarks
        if len(multi_hand_landmarks) != 2:
            return False

        hands = self._get_hands_by_label(multi_hand_landmarks, multi_handedness)

        if "Left" not in hands or "Right" not in hands:
            return False
        
        left, right = hands["Left"], hands["Right"]

        left_thumb = left.landmark[self.THUMB_TIP]
        right_thumb = right.landmark[self.THUMB_TIP]

        left_index = left.landmark[self.INDEX_TIP]
        right_index = right.landmark[self.INDEX_TIP]

        thumb_distance = self._distance(left_thumb, right_thumb)
        index_distance = self._distance(left_index, right_index)

        #return
        return thumb_distance < threshold and index_distance < threshold


