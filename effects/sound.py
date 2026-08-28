import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.tracks = {}
    
    def load(self, name, filepath):
        self.tracks[name] = filepath
    
    def play(self, name):
        if name not in self.tracks:
            return
        pygame.mixer.music.load(self.tracks[name])
        pygame.mixer.music.play()
    
    def stop(self):
        pygame.mixer.music.stop()