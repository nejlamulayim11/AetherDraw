from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class FingerState:
    thumb: bool = False
    index: bool = False
    middle: bool = False
    ring: bool = False
    pinky: bool = False


@dataclass
class HandData:
    landmarks: List[Tuple[int, int, int]]

    wrist: Tuple[int, int]
    thumb_tip: Tuple[int, int]
    index_tip: Tuple[int, int]
    middle_tip: Tuple[int, int]
    ring_tip: Tuple[int, int]
    pinky_tip: Tuple[int, int]

    fingers: FingerState

    is_left: bool
    is_right: bool