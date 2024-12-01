# tests/test_store.py
import pytest
from src.store.store import DistributedStore, StorageEntry
from src.store.consistency import ConsistencyManager, ConsistencyLevel, WriteResult, ReadResult
import time
import threading

@pytest.fixture
def store():
    return DistributedStore()

@pytest.fixture
def consistency_manager():
    return ConsistencyManager(node_count=3)

def test_basic_operations(store):
    # Test create
    assert store.create("key1", "value1")
    assert not store.create("key1", "value2")  # Duplicate key

    # Test read
    assert store.read("key1") == "value1"
    assert store.read("nonexistent") is None

    # Test update
    assert store.update("key1", "new_value")
    assert store.read("key1") == "new_value"
    assert not store.update("nonexistent", "value")

    # Test delete
    assert store.delete("key1")
    assert not store.delete("key1")  # Already deleted
    assert store.read("key1") is None

def test_concurrent_access(store):
    def concurrent_writes():
        for i in range(100):
            store.create(f"key_{i}", f"value_{i}")

    threads = [threading.Thread(target=concurrent_writes) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify all writes were successful and thread-safe
    for i in range(100):
        assert store.read(f"key_{i}") == f"value_{i}"

def test_versioning(store):
    store.create("key1", "value1")
    initial_version = store.get_version("key1")
    
    store.update("key1", "value2")
    new_version = store.get_version("key1")
    
    assert new_version > initial_version

def test_merge_operation(store):
    # Create some data in the main store
    store.create("key1", "value1")
    store.create("key2", "value2")

    # Create another store's data to merge
    other_store = {
        "key1": ("new_value1", 2, time.time()),  # Higher version
        "key3": ("value3", 1, time.time())       # New key
    }

    store.merge(other_store)

    assert store.read("key1") == "new_value1"  # Updated value
    assert store.read("key2") == "value2"      # Unchanged
    assert store.read("key3") == "value3"      # New key

def test_consistency_levels(consistency_manager):
    # Test ONE consistency
    assert consistency_manager.get_required_acks(ConsistencyLevel.ONE) == 1

    # Test QUORUM consistency (for 3 nodes, quorum is 2)
    assert consistency_manager.get_required_acks(ConsistencyLevel.QUORUM) == 2

    # Test ALL consistency
    assert consistency_manager.get_required_acks(ConsistencyLevel.ALL) == 3

def test_write_result():
    write_result = WriteResult()
    write_result.add_ack("node1")
    write_result.add_ack("node2")

    assert write_result.ack_count == 2
    assert "node1" in write_result.acks
    assert "node2" in write_result.acks

def test_read_result():
    read_result = ReadResult()
    read_result.value = "test_value"
    read_result.version = 1
    read_result.node_id = "node1"

    assert read_result.value == "test_value"
    assert read_result.version == 1
    assert read_result.node_id == "node1"