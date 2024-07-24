from datetime import datetime
import os
import cv2
from djitellopy import Tello

class PhotoCapture:
    def __init__(self, drone, media_dir="media"):
        self.drone = drone
        self.media_dir = media_dir
        os.makedirs(self.media_dir, exist_ok=True)

    def take_photo(self):
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
        photo_path = os.path.join(self.media_dir, f'photo-{date_time}.jpg')
        cv2.imwrite(photo_path, self.drone.get_frame_read().frame)
        print(f"Photo taken and saved to {photo_path}")
