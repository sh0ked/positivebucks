from enum import Enum


class OrderStatuses(Enum):
    UNKNOWN = 0
    WAITING = 1
    ACTIVE = 2
    COMPLETED = 3
