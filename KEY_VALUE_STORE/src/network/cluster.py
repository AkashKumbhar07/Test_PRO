from typing import List, Set, Any
import requests

class ClusterManager:
    def __init__(self, node_address: str, seed_nodes: List[str]):
        self.node_address = node_address
        self.nodes: Set[str] = set(seed_nodes)
        
    def broadcast_update(self, key: str, value: Any, operation: str):
        for node in self.nodes:
            if node != self.node_address:
                try:
                    requests.post(f"{node}/sync", 
                                json={
                                    'key': key,
                                    'value': value,
                                    'operation': operation
                                })
                except requests.RequestException:
                    # Handle node failure
                    pass

    def add_node(self, node_address: str):
        self.nodes.add(node_address)

    def remove_node(self, node_address: str):
        self.nodes.remove(node_address)
