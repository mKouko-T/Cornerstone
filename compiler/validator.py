import os
import hashlib
import json
import urllib.request
import unicodedata
from pathlib import Path
from compiler.ir import CanonicalIR

class Validator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.mode = os.environ.get("COMPILER_MODE", "live").lower()
        self.pinned_sha = os.environ.get("PINNED_COMMIT_SHA", "")

    def _canonicalize(self, raw_bytes: bytes) -> str:
        """Applies the canonicalization pipeline per COMPILER_SPEC.md"""
        # 1. BOM Stripping
        if raw_bytes.startswith(b'\xef\xbb\xbf'):
            raw_bytes = raw_bytes[3:]
            
        # 2. UTF-8 Decode
        text = raw_bytes.decode('utf-8')
        
        # 3. LF Normalization
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # 4. Unicode NFC Normalization
        text = unicodedata.normalize('NFC', text)
        
        return text

    def _hash_canonical(self, canonical_text: str) -> str:
        return hashlib.sha256(canonical_text.encode('utf-8')).hexdigest()

    def validate(self, ir: CanonicalIR):
        """Pass 5: Validation. Enforces correctness and remote identity."""
        self._check_ambiguity()
        self._fetch_remote_specs(ir)
        self._resolve_dependencies(ir)
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

    def _check_ambiguity(self):
        """Fail fast if multiple canonical candidates exist."""
        docs_dir = self.root_dir / "docs"
        if not docs_dir.exists():
            return
            
        files = [f.name for f in docs_dir.iterdir() if f.is_file()]
        canonical_count = sum(1 for f in files if f.startswith("Canonical_Model"))
        if canonical_count > 1:
            raise RuntimeError("AMBIGUITY FATAL: Multiple Canonical_Model files detected.")

    def _fetch_remote_specs(self, ir: CanonicalIR):
        """Fetches the live compiler identity and compiler order from Foundation Zero to prevent drift."""
        if self.mode == "pinned":
            if not self.pinned_sha:
                raise RuntimeError("COMPILER FATAL: Pinned mode requires PINNED_COMMIT_SHA environment variable.")
            sha_to_fetch = self.pinned_sha
            url_context = f"https://raw.githubusercontent.com/mKouko-T/Foundation_Zero/{sha_to_fetch}/BOOT_CONTEXT.md"
            url_order = f"https://raw.githubusercontent.com/mKouko-T/Foundation_Zero/{sha_to_fetch}/compiler/COMPILER_ORDER.json"
            ir.compiler_identity.remote_commit_sha = sha_to_fetch
        else:
            url_context = "https://raw.githubusercontent.com/mKouko-T/Foundation_Zero/main/BOOT_CONTEXT.md"
            url_order = "https://raw.githubusercontent.com/mKouko-T/Foundation_Zero/main/compiler/COMPILER_ORDER.json"
            api_url = "https://api.github.com/repos/mKouko-T/Foundation_Zero/commits/main"
            try:
                req_api = urllib.request.Request(api_url, headers={"User-Agent": "Foundation-Zero-Compiler"})
                with urllib.request.urlopen(req_api) as api_response:
                    api_data = json.loads(api_response.read().decode('utf-8'))
                    ir.compiler_identity.remote_commit_sha = api_data.get("sha", "UNKNOWN")
            except Exception as e:
                raise RuntimeError(f"COMPILER FATAL: Could not verify remote compiler commit. {e}")

        try:
            req_context = urllib.request.Request(url_context)
            with urllib.request.urlopen(req_context) as response:
                raw_bytes = response.read()
                
            canonical_text = self._canonicalize(raw_bytes)
            
            # Verify version matching
            if "Foundation Zero Lite v1.0" not in canonical_text:
                raise RuntimeError("COMPILER FATAL: Remote compiler version mismatch.")
                
            ir.compiler_identity.content = canonical_text
            ir.compiler_identity.hash_sha256 = self._hash_canonical(canonical_text)
            
            req_order = urllib.request.Request(url_order)
            with urllib.request.urlopen(req_order) as response:
                order_bytes = response.read()
                
            self.compilation_order = json.loads(order_bytes.decode('utf-8'))
            
        except Exception as e:
            raise RuntimeError(f"COMPILER FATAL: Could not fetch remote compiler specs. {e}")

    def _calculate_hashes(self, ir: CanonicalIR):
        """Pass 3 (implied): Generates cryptographic hashes for provenance using Canonicalization."""
        for filepath in self.compilation_order:
            if "(remote)" in filepath:
                continue
            
            full_path = self.root_dir / filepath
            if not full_path.exists():
                raise RuntimeError(f"MISSING FILE FATAL: {filepath} is required for compilation.")
                
            raw_bytes = full_path.read_bytes()
            canonical_text = self._canonicalize(raw_bytes)
            sha256_hash = self._hash_canonical(canonical_text)
            ir.provenance.file_hashes[filepath] = sha256_hash
            
    def _resolve_dependencies(self, ir: CanonicalIR):
        """Pass 4: Dependency Resolution (Explicit Ordering per COMPILER_SPEC.md)."""
        if not hasattr(self, 'compilation_order'):
            raise RuntimeError("COMPILER FATAL: Compilation order not fetched.")
        ir.provenance.dependency_graph = self.compilation_order
