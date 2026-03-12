#TODO: check color and use pallet? or create a standard pallet for status defaults
from enums import StatusCategory

DEFAULT_SPRINT_STATUSES = [
    {"name": "Planned",    "color": "#6b7280", "order": 0, "isDefault": True,  "isClosed": False},
    {"name": "Active",     "color": "#f59e0b", "order": 1, "isDefault": False, "isClosed": False},
    {"name": "Completed",  "color": "#10b981", "order": 2, "isDefault": False, "isClosed": True},
    {"name": "Cancelled",  "color": "#ef4444", "order": 3, "isDefault": False, "isClosed": True},
]



DEFAULT_STATUSES = [
    {"name": "Backlog",     "color": "#6b7280", "order": 0, "isDefault": True,  "isClosed": False, "category": StatusCategory.NOT_STARTED},
    {"name": "Todo",        "color": "#3b82f6", "order": 1, "isDefault": False, "isClosed": False, "category": StatusCategory.NOT_STARTED},
    {"name": "In Progress", "color": "#f59e0b", "order": 2, "isDefault": False, "isClosed": False, "category": StatusCategory.STARTED},
    {"name": "In Review",   "color": "#8b5cf6", "order": 3, "isDefault": False, "isClosed": False, "category": StatusCategory.STARTED},
    {"name": "Done",        "color": "#10b981", "order": 4, "isDefault": False, "isClosed": True,  "category": StatusCategory.COMPLETED},
    {"name": "Cancelled",   "color": "#ef4444", "order": 5, "isDefault": False, "isClosed": True,  "category": StatusCategory.CANCELLED},
]

