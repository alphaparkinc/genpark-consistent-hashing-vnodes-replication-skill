"""Consistent Hashing Ring with Virtual Nodes and Replication.
100% Python Standard Library.
"""

import hashlib
import bisect

class ConsistentHashRing:
    """Consistent hashing ring with virtual nodes (vnodes) and replication."""
    def __init__(self, vnodes=10):
        self.vnodes = vnodes
        self.ring = []
        self.nodes = set()

    @staticmethod
    def _hash(key):
        return int(hashlib.md5(str(key).encode("utf-8")).hexdigest()[:8], 16)

    def add_node(self, node_id):
        self.nodes.add(node_id)
        for i in range(self.vnodes):
            v_key = f"{node_id}#vnode{i}"
            h = self._hash(v_key)
            bisect.insort(self.ring, (h, node_id))

    def remove_node(self, node_id):
        self.nodes.discard(node_id)
        self.ring = [item for item in self.ring if item[1] != node_id]

    def get_node(self, key):
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, (h, ""))
        if idx == len(self.ring):
            idx = 0
        return self.ring[idx][1]

    def get_replicas(self, key, num_replicas=3):
        if not self.ring:
            return []
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, (h, ""))
        replicas = []
        n = len(self.ring)
        for i in range(n):
            cur_idx = (idx + i) % n
            nid = self.ring[cur_idx][1]
            if nid not in replicas:
                replicas.append(nid)
                if len(replicas) == min(num_replicas, len(self.nodes)):
                    break
        return replicas
