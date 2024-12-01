# tests/test_network.py
import pytest
from src.network.cluster import ClusterManager
from src.network.discovery import NodeDiscovery
import requests
from unittest.mock import patch, Mock
import threading
import time

@pytest.fixture
def cluster_manager():
    return ClusterManager(
        node_address="http://localhost:8000",
        seed_nodes=["http://localhost:8001", "http://localhost:8002"]
    )

@pytest.fixture
def node_discovery():
    discovery = NodeDiscovery(
        node_address="http://localhost:8000",
        seed_nodes=["http://localhost:8001", "http://localhost:8002"]
    )
    return discovery

def test_cluster_initialization(cluster_manager):
    assert cluster_manager.node_address == "http://localhost:8000"
    assert len(cluster_manager.nodes) == 2
    assert "http://localhost:8001" in cluster_manager.nodes
    assert "http://localhost:8002" in cluster_manager.nodes

def test_add_remove_node(cluster_manager):
    # Add new node
    new_node = "http://localhost:8003"
    cluster_manager.add_node(new_node)
    assert new_node in cluster_manager.nodes
    assert len(cluster_manager.nodes) == 3

    # Remove node
    cluster_manager.remove_node(new_node)
    assert new_node not in cluster_manager.nodes
    assert len(cluster_manager.nodes) == 2

@patch('requests.post')
def test_broadcast_update(mock_post, cluster_manager):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    cluster_manager.broadcast_update("test_key", "test_value", "create")
    
    # Should make two POST requests (one for each seed node)
    assert mock_post.call_count == 2

def test_node_discovery_registration(node_discovery):
    # Test node registration
    new_node = "http://localhost:8003"
    assert node_discovery.register_node(new_node)
    assert new_node in node_discovery.get_nodes()

    # Test duplicate registration
    assert not node_discovery.register_node(new_node)

def test_node_discovery_removal(node_discovery):
    new_node = "http://localhost:8003"
    node_discovery.register_node(new_node)
    assert node_discovery.remove_node(new_node)
    assert new_node not in node_discovery.get_nodes()

@patch('requests.post')
def test_heartbeat_mechanism(mock_post, node_discovery):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Start discovery service
    node_discovery.start()
    time.sleep(6)  # Wait for one heartbeat interval

    # Should have attempted to send heartbeats to seed nodes
    assert mock_post.call_count > 0

    # Clean up
    node_discovery.stop()