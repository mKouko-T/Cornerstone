import os
import re
import unicodedata
from pathlib import Path
from compiler.ir import CanonicalIR

class Parser:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
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
        return text.strip()

    def parse(self, ir: CanonicalIR):
        """Pass 2: Parsing. Reads raw files and populates the semantic IR."""
        
        # 1. Parse Runtime Rules
        ir.knowledge_state.runtime_rules = self._read_file("docs/Runtime_Contract.md")
        
        # 2. Parse Canonical Model
        ir.knowledge_state.canonical_model = self._read_file("docs/Canonical_Model.md")
        
        # 3. Parse Methodology
        ir.knowledge_state.methodology = self._read_file("docs/Genesis_Methodology.md")
        
        # 4. Parse Task State
        ir.execution_context.task_state = self._read_file("task.md")
        
        # 5. Parse Bootstrap Context for specific metadata
        self._parse_bootstrap(ir)
        
        # 6. Fetch local Git Commit SHA
        self._fetch_local_git_sha(ir)
        
    def _fetch_local_git_sha(self, ir: CanonicalIR):
        import subprocess
        try:
            result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(self.root_dir), capture_output=True, text=True, check=True)
            ir.repository_identity.commit_sha = result.stdout.strip()
            
            # Check for dirty working tree
            status = subprocess.run(["git", "status", "--porcelain"], cwd=str(self.root_dir), capture_output=True, text=True, check=True)
            if status.stdout.strip():
                ir.repository_identity.commit_sha = "DIRTY"
        except Exception:
            ir.repository_identity.commit_sha = "UNKNOWN"
        
    def _read_file(self, filepath: str) -> str:
        full_path = self.root_dir / filepath
        if not full_path.exists():
            raise RuntimeError(f"MISSING FILE FATAL: {filepath} is required for compilation.")
        raw_bytes = full_path.read_bytes()
        return self._canonicalize(raw_bytes)

    def _parse_bootstrap(self, ir: CanonicalIR):
        """Extracts structural meaning from BOOTSTRAP.md"""
        content = self._read_file("BOOTSTRAP.md")
        
        # Extract Mission
        mission_match = re.search(r"## Mission\n(.*?)\n##", content, re.DOTALL)
        if mission_match:
            ir.execution_context.mission = mission_match.group(1).strip()
            
        # Extract Phase
        phase_match = re.search(r"## Current Phase\n(.*?)\n##", content, re.DOTALL)
        if phase_match:
            ir.execution_context.phase = phase_match.group(1).strip()
            
        # Extract Constraints
        constraints_match = re.search(r"## Active Constraints\n(.*?)\n##", content, re.DOTALL)
        if constraints_match:
            constraints_text = constraints_match.group(1).strip()
            ir.execution_context.constraints = [
                line.strip("- ").strip() for line in constraints_text.split("\n") if line.strip()
            ]
