# genpark-api-spec-evolution-and-breaking-change-impact-analyzer-skill

Semantic API specification diff analyzer, schema breaking change detector, and downstream agent compatibility evaluator.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Semantic Schema Diffing**: Compares two OpenAPI/JSON-RPC schemas at the endpoint, method, and parameter level.
- **Breaking Change Detection**: Identifies removed routes, deleted methods, and newly introduced required parameters that break legacy clients.
- **Downstream Agent Tool Compatibility Verdict**: Generates immediate pass/fail evaluations for autonomous agent tool execution layers.

## Architecture

```
[Old API Spec + New API Spec (OpenAPI/JSON)]
                      │
                      ▼
┌──────────────────────────────────────────────────┐
│              APISpecDiffAnalyzer                 │
│  - Endpoint Route Addition/Deletion Checker      │
│  - HTTP Method Parity Comparator                 │
│  - Parameter Required/Optional Mutation Scanner  │
└──────────────────────────────────────────────────┘
                      │
                      ▼
[Backward Compatibility Verdict + Breaking Changes List]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `analyze_api_spec_diff`: Compares two OpenAPI/JSON-RPC specification versions for breaking parameter and endpoint changes.

## Quickstart (Python API)

```python
from client import APISpecDiffAnalyzer

v1 = {"paths": {"/item": {"get": {"parameters": []}}}}
v2 = {"paths": {"/item": {"get": {"parameters": [{"name": "id", "required": True}]}}}}

diff = APISpecDiffAnalyzer.compare_specs(v1, v2)
print("Compatible:", diff["is_backward_compatible"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
