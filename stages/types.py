from typing import Callable
import numpy as np

__all__ = [
    '_Image',
    '_Layer',
    '_ImageStage',
    '_LayerStage',
    '_NullStage',
    'Callable',
]

_Image = np.ndarray  # 3D array of pixels
_Layer = np.ndarray  # 2D array of pixels
_ImageStage = Callable[[], _Image]
_LayerStage = Callable[[], _Layer]
_NullStage = Callable[[], None]
