from .types import *
import cv2 as cv

def ImageFileSink(filename: str):
    def stage(prev_stage: _ImageStage) -> _NullStage:
        def sink() -> None:
            image = prev_stage()
            print('sinking file')
            cv.imwrite(filename, image)
            return
        return sink
    return stage
