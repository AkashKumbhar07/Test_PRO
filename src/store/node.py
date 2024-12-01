# src/store/node.py
from typing import Optional, Dict, Any, List
import uuid
import time
from dataclasses import dataclass
from enum import Enum

class NodeState(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPECT = "suspect"

@dataclass
class NodeMetadata:
    node_id: str
    address: str
    state: NodeState
    last_heartbeat: float
    version: int

class Node:
    def __init__(self, address: str):
        self.node_id = str(uuid.uuid4())
        self.address = address
        self.state = NodeState.ACTIVE
        self.last_heartbeat = time.time()
        self.version = 0
        self.peers: Dict[str, NodeMetadata] = {}

    def update_heartbeat(self):
        """Update the last heartbeat timestamp"""
        self.last_heartbeat = time.time()

    def add_peer(self, address: str, node_id: str) -> None:
        """Add or update a peer node"""
        self.peers[node_id] = NodeMetadata(
            node_id=node_id,
            address=address,
            state=NodeState.ACTIVE,
            last_heartbeat=time.time(),
            version=0
        )

    def remove_peer(self, node_id: str) -> bool:
        """Remove a peer node"""
        if node_id in self.peers:
            del self.peers[node_id]
            return True
        return False

    def update_peer_state(self, node_id: str, state: NodeState) -> bool:
        """Update the state of a peer node"""
        if node_id in self.peers:
            peer = self.peers[node_id]
            peer.state = state
            return True
        return False

    def get_active_peers(self) -> List[NodeMetadata]:
        """Get all active peers"""
        return [peer for peer in self.peers.values() 
                if peer.state == NodeState.ACTIVE]

    def check_peer_health(self, heartbeat_timeout: float = 10.0) -> None:
        """Check health of all peers and mark suspicious nodes"""
        current_time = time.time()
        for node_id, peer in self.peers.items():
            if (current_time - peer.last_heartbeat) > heartbeat_timeout:
                if peer.state == NodeState.ACTIVE:
                    peer.state = NodeState.SUSPECT
                elif peer.state == NodeState.SUSPECT:
                    peer.state = NodeState.INACTIVE

    def update_peer_heartbeat(self, node_id: str) -> bool:
        """Update the heartbeat of a peer node"""
        if node_id in self.peers:
            peer = self.peers[node_id]
            peer.last_heartbeat = time.time()
            if peer.state == NodeState.SUSPECT:
                peer.state = NodeState.ACTIVE
            return True
        return False

    def get_node_info(self) -> Dict[str, Any]:
        """Get information about this node"""
        return {
            "node_id": self.node_id,
            "address": self.address,
            "state": self.state.value,
            "version": self.version,
            "peer_count": len(self.peers),
            "active_peer_count": len(self.get_active_peers())
        }