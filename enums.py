from enum import Enum


class Status(str, Enum):
    ERROR = 'error'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    TO_DO = 'to_do'
    OPEN = 'open'
