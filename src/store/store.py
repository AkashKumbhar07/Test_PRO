from threading import Lock
from typing import Dict, Optional, Any, List, Tuple
import time
import uuid

class StorageEntry:
    def __init__(self, value: Any, version: int, timestamp: float):
        self.value = value
        self.version = version
        self.timestamp = timestamp
        self.node_id = str(uuid.uuid4())

class DistributedStore:
    def __init__(self):
        self._store: Dict[str, StorageEntry] = {}
        self._lock = Lock()
        self._version = 0
        self._node_id = str(uuid.uuid4())

    def create(self, key: str, value: Any) -> bool:
        with self._lock:
            if key in self._store:
                return False
            
            entry = StorageEntry(
                value=value,
                version=self._version + 1,
                timestamp=time.time()
            )
            self._store[key] = entry
            self._version += 1
            return True

    def read(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._store:
                return None
            return self._store[key].value

    def update(self, key: str, value: Any) -> bool:
        with self._lock:
            if key not in self._store:
                return False
            
            entry = StorageEntry(
                value=value,
                version=self._store[key].version + 1,
                timestamp=time.time()
            )
            self._store[key] = entry
            self._version += 1
            return True

    def delete(self, key: str) -> bool:
        with self._lock:
            if key not in self._store:
                return False
            del self._store[key]
            self._version += 1
            return True

    def get_version(self, key: str) -> Optional[int]:
        with self._lock:
            if key not in self._store:
                return None
            return self._store[key].version

    def get_all_entries(self) -> List[Tuple[str, Any, int]]:
        """Return all entries as (key, value, version) tuples"""
        with self._lock:
            return [(key, entry.value, entry.version) 
                    for key, entry in self._store.items()]

    def merge(self, other_store: Dict[str, Tuple[Any, int, float]]):
        """Merge another store's entries based on version and timestamp"""
        with self._lock:
            for key, (value, version, timestamp) in other_store.items():
                if key not in self._store or (
                    version > self._store[key].version or
                    (version == self._store[key].version and 
                     timestamp > self._store[key].timestamp)
                ):
                    self._store[key] = StorageEntry(value, version, timestamp)
                    self._version = max(self._version, version)