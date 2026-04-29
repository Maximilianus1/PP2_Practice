import pygame
import os

class MusicPlayer:


    def __init__(self):
        music_folder = "music"
        pygame.mixer.init()
        self.tracks = []
        #collect all exsisted tracks from folder music
        for file in sorted(os.listdir(music_folder)):
            if file.endswith((".wav", ".mp3")):
                self.tracks.append(os.path.join(music_folder, file))
        #Error handler
        if not self.tracks:
            print("No music files found in music folder!")
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        pygame.mixer.music.set_volume(0.5)
    def play(self):
        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
    def pause(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
    def unpause(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
    def toggle_pause(self):
        if self.is_paused:
            self.unpause()
        else:
            self.pause()
    def next(self):
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.play()
    def previous(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.play()
    def get_current_track(self):
        return os.path.basename(self.tracks[self.current_index])
    def get_position(self):
        return pygame.mixer.music.get_pos()
    def set_volume(self, volume):
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)
    def volume_up(self, step=0.1):
        current = pygame.mixer.music.get_volume()
        self.set_volume(current+step)
    def volume_down(self, step=0.1):
        current = pygame.mixer.music.get_volume()
        self.set_volume(current - step)
    def get_volume(self):
        return pygame.mixer.music.get_volume()