"""Example usage for API Specification Evolution & Breaking Change Impact Analyzer."""
from client import APISpecDiffAnalyzer

if __name__ == "__main__":
    v1 = {
        "paths": {
            "/api/v1/orders": {
                "post": {
                    "parameters": [{"name": "product_id", "required": True}],
                }
            }
        }
    }

    # v2 introduces a new required parameter 'customer_email' -> Breaking change!
    v2 = {
        "paths": {
            "/api/v1/orders": {
                "post": {
                    "parameters": [
                        {"name": "product_id", "required": True},
                        {"name": "customer_email", "required": True},
                    ],
                }
            }
        }
    }

    diff = APISpecDiffAnalyzer.compare_specs(v1, v2)
    print("Backward Compatible:", diff["is_backward_compatible"])
    print("Verdict:", diff["agent_compatibility_verdict"])
    for b in diff["breaking_changes"]:
        print(f"  - [{b['severity']}] {b['type']}: {b['detail']}")
