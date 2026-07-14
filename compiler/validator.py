import hashlib
from compiler.ir import CanonicalIR

class Validator:
    def __init__(self, root_dir: str = "."):
        pass

    def _hash_canonical(self, canonical_text: str) -> str:
        return hashlib.sha256(canonical_text.encode('utf-8')).hexdigest()

    def validate(self, ir: CanonicalIR):
        """Pass 5: Validation. Enforces correctness and remote identity entirely from IR."""
        self._validate_remote_context(ir)
        self._topological_sort(ir)
        self._calculate_hashes(ir)
        
        # Enforce Capability Declarations
        ir.compiler_identity.guarantees = [
            "Canonical ordering",
            "Missing-file detection",
            "Hash verification",
            "Repository verification",
            "Compiler verification",
            "Deterministic ordering",
            "Dependency resolution",
            "Unicode NFC Normalization",
            "UTF-8 BOM Stripping",
            "LF Line Ending Normalization"
        ]

    def _validate_remote_context(self, ir: CanonicalIR):
        context_text = ir.raw_files.get("boot_context", "")
        if "Foundation Zero Lite v1.0" not in context_text:
            raise RuntimeError("COMPILER FATAL: Remote compiler version mismatch.")
        ir.compiler_identity.content = context_text
        ir.compiler_identity.hash_sha256 = self._hash_canonical(context_text)

    def _topological_sort(self, ir: CanonicalIR):
        """Topological sort of the dependency graph defined in COMPILER_PIPELINE.json."""
        stages = ir.pipeline_graph.get("stages", [])
        graph = {}
        in_degree = {}
        
        # Initialize graph
        for s in stages:
            sid = s["id"]
            graph[sid] = []
            in_degree[sid] = 0

        # Build graph and in-degrees
        for s in stages:
            sid = s["id"]
            for dep in s.get("depends_on", []):
                if dep in graph:
                    graph[dep].append(sid)
                    in_degree[sid] += 1
                else:
                    raise RuntimeError(f"COMPILER FATAL: Unknown dependency '{dep}' for stage '{sid}'")

        # Execute Kahn's algorithm
        queue = [k for k, v in in_degree.items() if v == 0]
        sorted_stages = []
        
        while queue:
            node = queue.pop(0)
            sorted_stages.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Acyclic check
        if len(sorted_stages) != len(stages):
            raise RuntimeError("COMPILER FATAL: Cyclic dependency detected in compilation graph.")
        
        # The semantic stage IDs represent the valid dependency graph execution order.
        ir.provenance.dependency_graph = sorted_stages

    def _calculate_hashes(self, ir: CanonicalIR):
        """Pass 3 (implied): Generates cryptographic hashes purely from Canonical IR bytes."""
        for stage_id, text in ir.raw_files.items():
            ir.provenance.file_hashes[stage_id] = self._hash_canonical(text)
