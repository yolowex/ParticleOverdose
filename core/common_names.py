import math
import random
import json
import pygame as pg
from pygame.locals import *
from typing import Optional

from pygame import Vector2,Surface,Color
if __import__("sys").platform == "emscripten":
    # PLATFORM = 'web'
    from core.pygame_ce.FRect import Rect as FRect
else:
    from pygame import FRect
