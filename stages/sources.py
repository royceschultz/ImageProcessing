from .types import *
import cv2 as cv

def ImageFileSource(filename: str):
    def stage() -> _ImageStage:
        def source() -> _Image:
            print('reading file')
            return cv.imread(filename)
        return source
    return stage


def VariableSource(image: _Image = None):
    # A lot like React.useState
    def stage() -> _ImageStage:
        def source() -> _Image:
            return image
        return source

    def setImage(new_image: _Image):
        nonlocal image
        image = new_image
    return stage, setImage
