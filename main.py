import pygame
import cv2
from datetime import datetime
import os
from threading import Thread
from time import sleep
from djitellopy import Tello
from video_recorder import VideoRecorder
from photo_capture import PhotoCapture


class TelloApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tello Control")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)

        self.drone = Tello()
        self.drone.connect()
        self.drone.streamon()

        self.video_recorder = VideoRecorder(self.drone)
        self.photo_capture = PhotoCapture(self.drone)

        self.recording = False
        self.photo_captured = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            controls, direction_label = self.get_controls()
            self.drone.send_rc_control(*controls)

            frame = self.drone.get_frame_read().frame
            det_img = frame.copy()

            battery = self.drone.get_battery()
            self.overlay_text(det_img, f"Battery: {battery}%", (10, 30), self.white)

            if self.recording:
                self.overlay_text(det_img, "Recording...", (10, 70), self.blue)
            elif self.photo_captured:
                self.overlay_text(det_img, "Photo Captured", (10, 70), self.blue)

            self.overlay_text(det_img, f"Direction: {direction_label}", (10, 110), self.white)

            self.screen.fill(self.black)
            frame = cv2.cvtColor(det_img, cv2.COLOR_BGR2RGB)
            frame = pygame.image.frombuffer(frame.tostring(), det_img.shape[1::-1], "RGB")
            self.screen.blit(frame, (0, 0))

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        self.drone.streamoff()
        self.drone.land()
        self.video_recorder.stop_recording()

    def get_controls(self):
        lr, fb, ud, rot = 0, 0, 0, 0
        speed = 50
        direction_label = ""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            lr = -speed
            direction_label = "LEFT"
        elif keys[pygame.K_RIGHT]:
            lr = speed
            direction_label = "RIGHT"
        if keys[pygame.K_UP]:
            fb = speed
            direction_label = "FORWARD"
        elif keys[pygame.K_DOWN]:
            fb = -speed
            direction_label = "BACKWARD"
        if keys[pygame.K_w]:
            ud = speed
            direction_label = "UP"
        elif keys[pygame.K_s]:
            ud = -speed
            direction_label = "DOWN"
        if keys[pygame.K_a]:
            rot = -speed
            direction_label = "TURN LEFT"
        elif keys[pygame.K_d]:
            rot = speed
            direction_label = "TURN RIGHT"

        if keys[pygame.K_t]:
            self.drone.takeoff()
        if keys[pygame.K_l]:
            self.drone.land()
        if keys[pygame.K_r]:
            self.drone.emergency()
        if keys[pygame.K_v]:
            self.video_recorder.start_recording()
            self.recording = True
            self.photo_captured = False
        if keys[pygame.K_b]:
            self.video_recorder.stop_recording()
            self.recording = False
        if keys[pygame.K_p]:
            self.photo_capture.take_photo()
            self.photo_captured = True

        return [lr, fb, ud, rot], direction_label

    def overlay_text(self, img, text, pos, color):
        cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)


if __name__ == "__main__":
    app = TelloApp()
    app.run()
