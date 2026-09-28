from client import ConsistentHashRing

ring = ConsistentHashRing(vnodes=50)
for node in ["storage-node-A", "storage-node-B", "storage-node-C", "storage-node-D"]:
    ring.add_node(node)

key = "session_token_991823"
primary = ring.get_node(key)
replicas = ring.get_replicas(key, num_replicas=3)

print(f"Key '{key}' primary node: {primary}")
print(f"Key '{key}' replica set (N=3): {replicas}")
