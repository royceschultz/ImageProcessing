from .types import *
import numpy as np

def VSyncLoss():
    offset = 0

    def stage(prev_stage: _LayerStage) -> _LayerStage:
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
