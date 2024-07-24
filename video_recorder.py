from datetime import datetime
import os
import cv2
from threading import Thread, Event
from time import sleep
from djitellopy import Tello

class VideoRecorder:
    def __init__(self, drone, media_dir="media"):
        self.drone = drone
        self.keep_recording = Event()
        self.recording_thread = None
        self.media_dir = media_dir
        os.makedirs(self.media_dir, exist_ok=True)

    def start_recording(self):
        self.keep_recording.set()
        self.recording_thread = Thread(target=self._record_video)
        self.recording_thread.start()

    def stop_recording(self):
        self.keep_recording.clear()
        if self.recording_thread is not None:
            self.recording_thread.join()

    def _record_video(self):
        height, width, _ = self.drone.get_frame_read().frame.shape
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
        video_path = os.path.join(self.media_dir, f'{date_time}.avi')
        video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
        while self.keep_recording.is_set():
            frame = self.drone.get_frame_read().frame
            if frame is not None:
                video.write(frame)
            sleep(1 / 30)
        video.release()
