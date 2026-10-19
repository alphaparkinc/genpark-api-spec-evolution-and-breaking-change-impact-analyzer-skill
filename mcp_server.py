"""MCP server for API Specification Evolution & Breaking Change Impact Analyzer."""
import sys
import json
from client import APISpecDiffAnalyzer


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "analyze_api_spec_diff",
                    "description": "Compares two OpenAPI/JSON-RPC specification versions for breaking parameter and endpoint changes",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "old_spec": {"type": "object"},
                            "new_spec": {"type": "object"},
                        },
                        "required": ["old_spec", "new_spec"],
                    },
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "analyze_api_spec_diff":
            res = APISpecDiffAnalyzer.compare_specs(
                args.get("old_spec", {}),
                args.get("new_spec", {}),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
