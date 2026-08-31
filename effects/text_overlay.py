import cv2

class Banner:
    def __init__(self, text, target_x, target_y, color, font_scale=1.5, thickness=3, slide_speed=25, hold_frames=45):
        self.lines = text.split("/n")
        self.target_x = target_x
        self.target_y = target_y
        self.color = color
        self.font_scale = font_scale
        self.thickness = thickness
        self.slide_speed = slide_speed
        self.hold_frames = hold_frames
        self.line_height = int(45 * font_scale)

        line_widths = [
            cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0][0]
            for line in self.lines
        ]

        self.x = -max(line_widths)
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
        for i, line in enumerate(self.lines):
            line_y = self.target_y + i * self.line_height
            cv2.putText(
                frame, line, (int(self.x), line_y),
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
        

        