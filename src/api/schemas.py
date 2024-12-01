from dataclasses import dataclass
from typing import Optional, Any, Dict, List
from datetime import datetime

@dataclass
class KeyValuePair:
    key: str
    value: Any
    version: int
    timestamp: float

@dataclass
class NodeInfo:
    node_id: str
    address: str
    state: str