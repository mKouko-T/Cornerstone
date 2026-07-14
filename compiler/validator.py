import os
import hashlib
import json
import urllib.request
from pathlib import Path
from compiler.ir import CanonicalIR

class Validator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)

    def validate(self, ir: CanonicalIR):
        """Pass 5: Validation. Enforces correctness and remote identity."""
        self._check_ambiguity()
        self._fetch_remote_compiler(ir)
        self._calculate_hashes(ir)
        self._resolve_dependencies(ir)
        
        # If we reach here, validation passes.
        ir.compiler_identity.certification = "PASS"

    def _check_ambiguity(self):
        """Fail fast if multiple canonical candidates exist."""
        # A simple check: ensure there isn't a v2 of core docs floating around
        docs_dir = self.root_dir / "docs"
        if not docs_dir.exists():
            return
            
        files = [f.name for f in docs_dir.iterdir() if f.is_file()]
        canonical_count = sum(1 for f in files if f.startswith("Canonical_Model"))
        if canonical_count > 1:
            raise RuntimeError("AMBIGUITY FATAL: Multiple Canonical_Model files detected.")

    def _fetch_remote_compiler(self, ir: CanonicalIR):
        """Fetches the live compiler identity from Foundation Zero to prevent drift."""
        url = "https://raw.githubusercontent.com/mKouko-T/Foundation_Zero/main/BOOT_CONTEXT.md"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                
            # Verify version matching
            if "Foundation Zero Lite v1.0" not in content:
                raise RuntimeError("COMPILER FATAL: Remote compiler version mismatch.")
                
            ir.compiler_identity.content = content
            
            # Fetch the latest commit SHA for provenance (using GitHub API)
            api_url = "https://api.github.com/repos/mKouko-T/Foundation_Zero/commits/main"
            req_api = urllib.request.Request(api_url, headers={"User-Agent": "Foundation-Zero-Compiler"})
            with urllib.request.urlopen(req_api) as api_response:
                api_data = json.loads(api_response.read().decode('utf-8'))
                ir.compiler_identity.remote_commit_sha = api_data.get("sha", "UNKNOWN")
                
        except Exception as e:
            raise RuntimeError(f"COMPILER FATAL: Could not verify remote compiler. {e}")

    def _calculate_hashes(self, ir: CanonicalIR):
        """Pass 3 (implied): Generates cryptographic hashes for provenance."""
        required_files = [
            "docs/Runtime_Contract.md",
            "docs/Canonical_Model.md",
            "docs/Genesis_Methodology.md",
            "task.md",
            "BOOTSTRAP.md"
        ]
        
        for filepath in required_files:
            full_path = self.root_dir / filepath
            content = full_path.read_bytes()
            sha256_hash = hashlib.sha256(content).hexdigest()
            ir.file_hashes[filepath] = sha256_hash
            
    def _resolve_dependencies(self, ir: CanonicalIR):
        """Pass 4: Dependency Resolution."""
        ir.dependency_graph = list(ir.file_hashes.keys()) + ["Foundation_Zero/BOOT_CONTEXT.md (remote)"]
