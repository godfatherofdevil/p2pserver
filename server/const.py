from enum import Enum


class PeerTypes(str, Enum):
    guest = "guest"
    host = "host"


class GameStatus(int, Enum):
    waiting = 0
    active = 1
