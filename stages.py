import numpy as np
import cv2 as cv
from typing import Callable

_Image = np.ndarray # 3D array of pixels
_Layer = np.ndarray # 2D array of pixels
_ImageStage = Callable[[], _Image]
_LayerStage = Callable[[], _Layer]
_NullStage = Callable[[], None]

def ImageFileSink(filename:str):
    def stage(prev_stage:_ImageStage) -> _NullStage:
        def sink() -> None:
            image = prev_stage()
            print('sinking file')
            cv.imwrite(filename, image)
            return
        return sink
    return stage

def ImageFileSource(filename:str):
    def stage() -> _ImageStage:
        def source() -> _Image:
            print('reading file')
            return cv.imread(filename)
        return source
    return stage

def VariableSource(image:_Image = None):
    # A lot like React.useState
    def stage() -> _ImageStage:
        def source() -> _Image:
            return image
        return source
    def setImage(new_image:_Image):
        nonlocal image
        image = new_image
    return stage, setImage

def VSyncLoss():
    offset = 0
    def stage(prev_stage:_LayerStage) -> _LayerStage:
        def vloss() -> _Layer:
            print('vloss')
            nonlocal offset
            layer = prev_stage()
            for row in layer:
                row[:] = np.roll(row, int(offset))
                offset += np.random.random() * 6 - 3
            return layer
        return vloss
    return stage

def GetLayer(index:int):
    def stage(prev_stage:_ImageStage) -> _LayerStage:
        def get_layer() -> _Layer:
            image = prev_stage()
            assert isinstance(image, np.ndarray)
            return image[:, :, index]
        return get_layer
    return stage

def SetLayer(index:int):
    def stage(prev_stage:_ImageStage, layer_stage:_LayerStage) -> _ImageStage:
        def set_layer() -> _Image:
            image = prev_stage()
            layer = layer_stage()
            assert isinstance(image, np.ndarray)
            assert isinstance(layer, np.ndarray)
            image[:, :, index] = layer
            return image
        return set_layer
    return stage

def BGR2HLS():
    def stage(prev_stage:_ImageStage) -> _ImageStage:
        def bgr2hls() -> _Image:
            image = prev_stage()
            return cv.cvtColor(image, cv.COLOR_BGR2HLS)
        return bgr2hls
    return stage

def HLS2BGR():
    def stage(prev_stage:_ImageStage) -> _ImageStage:
        def hls2bgr() -> _Image:
            image = prev_stage()
            return cv.cvtColor(image, cv.COLOR_HLS2BGR)
        return hls2bgr
    return stage

def Then(*stages):
    def stage(prev_stage):
        p = prev_stage
        for s in stages:
            p = s(p)
        return p
    return stage

def Invert():
    def stage(prev_stage:_ImageStage) -> _ImageStage:
        def invert() -> _Image:
            image = prev_stage()
            return 255 - image
        return invert
    return stage

def AddMod(amount:int, modulo:int):
    def stage(prev_stage:_LayerStage) -> _LayerStage:
        def addmod() -> _Layer:
            layer = prev_stage()
            return (layer + amount) % modulo
        return addmod
    return stage

def ApplyToLayer(index:int, app_stage:Callable[[_LayerStage], _LayerStage]):
    def stage(prev_stage:_ImageStage) -> _ImageStage:
        setLayer = SetLayer(index)
        getLayer = GetLayer(index)
        return setLayer(prev_stage, app_stage(getLayer(prev_stage)))
    return stage

def Cache():
    def stage(prev_stage):
        cache = None
        def cache_stage():
            nonlocal cache
            if cache is None:
                cache = prev_stage()
            return cache
        return cache_stage
    return stage
