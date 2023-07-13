from .types import *
import numpy as np
from numba import jit

def VSyncLoss():
    offset = 0

    def stage(prev_stage: _LayerStage) -> _LayerStage:
        def vloss() -> _Layer:
            nonlocal offset
            layer = prev_stage()
            for row in layer:
                row[:] = np.roll(row, int(offset), axis=0)
                offset += np.random.random() * 2 - 1
                if np.random.random() < 0.001:
                    offset = 0
            return layer
        return vloss
    return stage

def SlowPhase(strength, max_phase=180):
    # This is a pretty slow stage
    def stage(prev_stage: _LayerStage) -> _LayerStage:
        def slow_phase() -> _Layer:
            layer = prev_stage()
            for row in layer:
                comp = np.exp(1j * row * 2 * np.pi / max_phase)

                w = 20
                kernel = np.ones(w) / w
                dtheta = np.angle(comp[1:] * np.conj(comp[:-1]))
                dtheta = np.append(dtheta, dtheta[-1]) # pad to match length
                dtheta = np.convolve(dtheta, kernel, mode='same')
                noise = np.exp(1j * 10 * dtheta * np.ones(len(row)) * 2 * np.pi)
                comp = comp * noise
                row[:] = (np.angle(comp) % (2 * np.pi)) * (max_phase / (2 * np.pi))
            return layer
        return slow_phase
    return stage
