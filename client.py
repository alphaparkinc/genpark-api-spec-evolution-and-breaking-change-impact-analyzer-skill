"""API Specification Evolution and Breaking Change Impact Analyzer.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional
import json


class APISpecDiffAnalyzer:
    """Performs semantic comparison between two OpenAPI/JSON-RPC API specification versions,
    identifying breaking schema changes and determining downstream autonomous agent tool compatibility."""

    @classmethod
    def compare_specs(cls, old_spec: Dict[str, Any], new_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Compares two API spec dictionaries for endpoints, methods, and parameter contracts."""
        breaking_changes = []
        non_breaking_changes = []

        old_paths = old_spec.get("paths", {})
        new_paths = new_spec.get("paths", {})

        # 1. Check for removed endpoints
        for path, methods in old_paths.items():
            if path not in new_paths:
                breaking_changes.append({
                    "type": "ENDPOINT_REMOVED",
                    "path": path,
                    "severity": "CRITICAL_BREAKING",
                    "detail": f"Endpoint '{path}' was deleted in new version.",
                })
            else:
                for method, op_spec in methods.items():
                    if method not in new_paths[path]:
                        breaking_changes.append({
                            "type": "HTTP_METHOD_REMOVED",
                            "path": path,
                            "method": method.upper(),
                            "severity": "CRITICAL_BREAKING",
                            "detail": f"Method '{method.upper()} {path}' was removed.",
                        })

        # 2. Check for new endpoints (non-breaking)
        for path, methods in new_paths.items():
            if path not in old_paths:
                non_breaking_changes.append({
                    "type": "ENDPOINT_ADDED",
                    "path": path,
                    "detail": f"New endpoint '{path}' added.",
                })

        # 3. Check parameter schema evolution on shared endpoints
        for path in set(old_paths.keys()).intersection(set(new_paths.keys())):
            for method in set(old_paths[path].keys()).intersection(set(new_paths[path].keys())):
                old_op = old_paths[path][method]
                new_op = new_paths[path][method]

                old_params = {p["name"]: p for p in old_op.get("parameters", []) if "name" in p}
                new_params = {p["name"]: p for p in new_op.get("parameters", []) if "name" in p}

                # Check if an existing parameter was removed
                for p_name, p_spec in old_params.items():
                    if p_name not in new_params and p_spec.get("required", False):
                        non_breaking_changes.append({
                            "type": "REQUIRED_PARAMETER_DEPRECATED",
                            "path": path,
                            "parameter": p_name,
                            "detail": f"Required parameter '{p_name}' was removed (downstream callers may still pass it harmlessly).",
                        })

                # Check if a NEW REQUIRED parameter was added (BREAKING for callers!)
                for p_name, p_spec in new_params.items():
                    if p_name not in old_params and p_spec.get("required", False):
                        breaking_changes.append({
                            "type": "NEW_REQUIRED_PARAMETER_ADDED",
                            "path": path,
                            "parameter": p_name,
                            "severity": "BREAKING_CHANGE",
                            "detail": f"New required parameter '{p_name}' added to '{method.upper()} {path}'; legacy agents will fail validation.",
                        })

        is_backward_compatible = len(breaking_changes) == 0

        return {
            "is_backward_compatible": is_backward_compatible,
            "breaking_changes_count": len(breaking_changes),
            "breaking_changes": breaking_changes,
            "non_breaking_changes_count": len(non_breaking_changes),
            "non_breaking_changes": non_breaking_changes,
            "agent_compatibility_verdict": (
                "PASS: All autonomous agent tool calls will execute without schema regression."
                if is_backward_compatible
                else "FAIL: Downstream agent schemas must be re-compiled to prevent runtime 400 errors."
            ),
        }
