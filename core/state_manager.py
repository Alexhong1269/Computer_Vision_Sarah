import time

class GestureStateManager:
    def __init__(self, debounce_frames=5, cooldown_seconds=1.0):
        #5 frames of a gesture
        self.debounce_frames = debounce_frames
        self.cooldown_seconds = cooldown_seconds

        #counting the gesture frames
        self.candidate_gesture = None
        self.candidate_count = 0

        #confirming that the gesture is real
        self.confirmed_gesture = None
        #cooldown for when the gesture last fired
        self.last_trigger_time = 0
    
    #building confidence on the gesture that we see
    def update(self, raw_gesture):
        if raw_gesture == self.candidate_gesture:
            self.candidate_count += 1
        else:
            self.candidate_gesture = raw_gesture
            self.candidate_count = 1
        
        if self.candidate_count > self.debounce_frames:
            self.confirmed_gesture = self.candidate_gesture
        #return
        return self.confirmed_gesture
    
    #mehtods for firing off the effects
    def can_trigger(self):
        return (time.time() - self.last_trigger_time) >= self.cooldown_seconds

    def trigger(self):
        self.last_trigger_time = time.time()
    

