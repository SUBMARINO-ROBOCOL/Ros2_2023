import cv2
import Codigo_ranas

def crop(frame, dim, is_singular=True):
    if is_singular:
        if dim > 0:
            frame = frame[dim:-dim, dim:-dim]
    Codigo_ranas.main(frame)



