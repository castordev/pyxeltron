from game.entities.ship import Ship
from render.constants import TILESET
from render.entities.base import BaseRender


class ShipRender(BaseRender):
    ENTITY_CLASS = Ship
    IMAGE_BANK = TILESET
    U = 0
    V = 0
    WIDTH = 8
    HEIGHT = 8
