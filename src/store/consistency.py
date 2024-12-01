from enum import Enum
from typing import List, Optional, Any
import time

class ConsistencyLevel(Enum):
    ONE = 1
    QUORUM = 2
    ALL = 3

class ConsistencyManager:
    def __init__(self, node_count: int):
        self.node_count = node_count
        self.quorum = (node_count // 2) + 1

    def get_required_acks(self, consistency: ConsistencyLevel) -> int:
        if consistency == ConsistencyLevel.ONE:
            return 1
        elif consistency == ConsistencyLevel.QUORUM:
            return self.quorum
        elif consistency == ConsistencyLevel.ALL:
            return self.node_count
        return self.quorum  # default to QUORUM

class WriteResult:
    def __init__(self):
        self.success = False
        self.timestamp = time.time()
        self.acks: List[str] = []

    def add_ack(self, node_id: str):
        self.acks.append(node_id)

    @property
    def ack_count(self) -> int:
        return len(self.acks)

class ReadResult:
    def __init__(self):
        self.value: Optional[Any] = None
        self.version: int = 0
        self.timestamp = time.time()
        self.node_id: Optional[str] = None