from .types import *


def Invert():
    def stage(prev_stage: _ImageStage) -> _ImageStage:
        def invert() -> _Image:
            image = prev_stage()
            return 255 - image
        return invert
    return stage


def AddMod(amount: int, modulo: int):
    def stage(prev_stage: _LayerStage) -> _LayerStage:
        def addmod() -> _Layer:
            layer = prev_stage()
            return (layer + amount) % modulo
        return addmod
    return stage
