# src/network/discovery.py
import time
import threading
import requests
from typing import Set, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NodeDiscovery:
    def __init__(self, node_address: str, seed_nodes: List[str], heartbeat_interval: int = 5):
        self.node_address = node_address
        self.nodes: Set[str] = set(seed_nodes)
        self.heartbeat_interval = heartbeat_interval
        self.is_running = False
        self._lock = threading.Lock()

    def start(self):
        """Start the node discovery service"""
        self.is_running = True
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop)
        self._heartbeat_thread.daemon = True
        self._heartbeat_thread.start()

    def stop(self):
        """Stop the node discovery service"""
        self.is_running = False
        if hasattr(self, '_heartbeat_thread'):
            self._heartbeat_thread.join()

    def _heartbeat_loop(self):
        """Continuously send heartbeats to other nodes"""
        while self.is_running:
            self._send_heartbeats()
            time.sleep(self.heartbeat_interval)

    def _send_heartbeats(self):
        """Send heartbeat to all known nodes"""
        dead_nodes = set()
        for node in self.nodes:
            if node != self.node_address:
                try:
                    response = requests.post(
                        f"{node}/heartbeat",
                        json={"sender": self.node_address},
                        timeout=2
                    )
                    if response.status_code != 200:
                        dead_nodes.add(node)
                except requests.RequestException:
                    dead_nodes.add(node)

        # Remove dead nodes
        with self._lock:
            self.nodes -= dead_nodes
            if dead_nodes:
                logger.info(f"Removed dead nodes: {dead_nodes}")

    def register_node(self, node_address: str):
        """Register a new node"""
        with self._lock:
            if node_address not in self.nodes:
                self.nodes.add(node_address)
                logger.info(f"Registered new node: {node_address}")
                return True
        return False

    def get_nodes(self) -> List[str]:
        """Get list of all known nodes"""
        with self._lock:
            return list(self.nodes)

    def remove_node(self, node_address: str):
        """Remove a node"""
        with self._lock:
            if node_address in self.nodes:
                self.nodes.remove(node_address)
                logger.info(f"Removed node: {node_address}")
                return True
        return False