from enum import Enum


class Status(str, Enum):
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    OPEN = 'open'
