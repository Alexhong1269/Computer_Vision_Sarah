import cv2

class Banner:
    def __init__(self, text, target_x, target_y, color, font_scale=1.5, thickness=3, slide_speed=25, hold_frames=45):
        self.text = text
        self.target_x = target_x
        self.target_y = target_y
        self.color = color
        self.font_scale = font_scale
        self.thickness = thickness
        self.slide_speed = slide_speed
        self.hold_frames = hold_frames

        (text_width, _ ), _ = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
        )

        self.x = -text_width
        self.arrived = False
        self.hold_counter = 0

    def update(self):
        if not self.arrived:
            self.x += self.slide_speed
            if self.x >= self.target_x:
                self.x = self.target_x
                self.arrived = True
        else:
            self.hold_counter += 1
    
    def is_alive(self):
        return not (self.arrived and self.hold_counter >= self.hold_frames)

    def draw(self, frame):
        cv2.putText(
            frame, self.text, (int(self.x), self.target_y),
            cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, self.color, self.thickness
        )
    
class BannerManager:
    def __init__(self):
        self.banners = []
    
    def show(self, text, target_x, target_y, color=(255, 255, 255)):
        self.banners.append(Banner(text, target_x, target_y, color))
    
    def update(self):
        for banner in self.banners:
            banner.update()
        self.banners = [b for b in self.banners if b.is_alive()]
    
    def draw(self, frame):
        for banner in self.banners:
            banner.draw(frame)
        

        