# Auteurs                 Date              Commentaires
#                          29 novembre 2022  Projet Intégration,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
# DESJARDINS Yoan
# BERGEVIN Émeric
#

import cv2 as cv
import time
from datetime import datetime
import numpy as np


class VideoCamera(object):
    def __init__(self, flip=False, file_type=".jpg", photo_string="stream_photo"):
        self.vs = cv.VideoCapture(0)
        self.vs.set(cv.CAP_PROP_FRAME_WIDTH, 320)
        self.vs.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
        self.flip = flip  # Flip frame vertically
        self.file_type = file_type  # image type i.e. .jpg
        self.photo_string = photo_string  # Name to save the photo
        time.sleep(2.0)

    def __del__(self):
        self.vs.release()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        ret_sts, frame = self.vs.read()
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()
