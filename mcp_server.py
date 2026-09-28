import sys
import json
from client import ConsistentHashRing

ring = ConsistentHashRing(vnodes=20)

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "consistent_hash_route",
                        "description": "Route key and generate replica set over consistent hash ring",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "nodes": {"type": "array", "items": {"type": "string"}},
                                "key": {"type": "string"},
                                "replicas": {"type": "integer", "default": 3}
                            },
                            "required": ["nodes", "key"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "consistent_hash_route":
            r = ConsistentHashRing(vnodes=20)
            for n in args["nodes"]:
                r.add_node(n)
            k = args["key"]
            num_rep = args.get("replicas", 3)
            primary = r.get_node(k)
            rep_list = r.get_replicas(k, num_replicas=num_rep)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"key": k, "primary_node": primary, "replica_set": rep_list})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
