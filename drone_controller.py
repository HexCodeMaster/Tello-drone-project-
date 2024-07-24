from datetime import datetime
import os
import cv2
import pygame
from djitellopy import Tello
from video_recorder import VideoRecorder
from photo_capture import PhotoCapture


class DroneController:
    def __init__(self):
        self.drone = Tello()
        try:
            self.drone.connect()
            self.drone.streamon()
            print(f'Battery level: {self.drone.get_battery()}%')
        except Exception as e:
            print(f'Error connecting to drone: {e}')
            exit(1)

        self.video_recorder = VideoRecorder(self.drone)
        self.photo_capture = PhotoCapture(self.drone)
        self.recording = False
        self.photo_captured = False

        pygame.init()
        pygame.display.set_mode((100, 100))

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

    def get_battery(self):
        return self.drone.get_battery()

    def is_recording(self):
        return self.recording

    def is_photo_captured(self):
        return self.photo_captured
