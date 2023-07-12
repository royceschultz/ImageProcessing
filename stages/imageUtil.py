import numpy as np
import cv2 as cv
from .types import *

def ApplyToLayer(index: int, app_stage: Callable[[_LayerStage], _LayerStage]):
    def stage(prev_stage: _ImageStage) -> _ImageStage:
        setLayer = SetLayer(index)
        getLayer = GetLayer(index)
        return setLayer(prev_stage, app_stage(getLayer(prev_stage)))
    return stage


def BGR2HLS():
    def stage(prev_stage: _ImageStage) -> _ImageStage:
        def bgr2hls() -> _Image:
            image = prev_stage()
            return cv.cvtColor(image, cv.COLOR_BGR2HLS)
        return bgr2hls
    return stage


def HLS2BGR():
    def stage(prev_stage: _ImageStage) -> _ImageStage:
        def hls2bgr() -> _Image:
            image = prev_stage()
            return cv.cvtColor(image, cv.COLOR_HLS2BGR)
        return hls2bgr
    return stage


def GetLayer(index: int):
    def stage(prev_stage: _ImageStage) -> _LayerStage:
        def get_layer() -> _Layer:
            image = prev_stage()
            assert isinstance(image, np.ndarray)
            return image[:, :, index]
        return get_layer
    return stage


def SetLayer(index: int):
    def stage(prev_stage: _ImageStage, layer_stage: _LayerStage) -> _ImageStage:
        def set_layer() -> _Image:
            image = prev_stage()
            layer = layer_stage()
            assert isinstance(image, np.ndarray)
            assert isinstance(layer, np.ndarray)
            image[:, :, index] = layer
            return image
        return set_layer
    return stage
