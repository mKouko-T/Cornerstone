import os
import re
import json
import urllib.request
import unicodedata
from pathlib import Path
from compiler.ir import CanonicalIR

class Parser:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.mode = os.environ.get("COMPILER_MODE", "live").lower()
        self.pinned_sha = os.environ.get("PINNED_COMMIT_SHA", "")

    def _canonicalize(self, raw_bytes: bytes) -> str:
        """Applies the canonicalization pipeline per COMPILER_SPEC.md"""
        if raw_bytes.startswith(b'\xef\xbb\xbf'):
            raw_bytes = raw_bytes[3:]
        text = raw_bytes.decode('utf-8')
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = unicodedata.normalize('NFC', text)
        return text.strip()

    def parse(self, ir: CanonicalIR):
        """Pass 2: Parsing. Reads raw files and populates the semantic IR."""
        self._fetch_remote_specs(ir)
        self._read_pipeline_artifacts(ir)
        self._parse_semantic_fields(ir)
        self._fetch_local_git_sha(ir)

    def _fetch_remote_specs(self, ir: CanonicalIR):
        """Fetches pipeline spec and context from Foundation Zero into IR."""
        if self.mode == "pinned":
            if not self.pinned_sha:
                raise RuntimeError("COMPILER FATAL: Pinned mode requires PINNED_COMMIT_SHA environment variable.")
            sha = self.pinned_sha
            url_context = f"https://raw.githubusercontent.com/mKouko-T/Foundation_Zero/{sha}/BOOT_CONTEXT.md"
            url_order = f"https://raw.githubusercontent.com/mKouko-T/Foundation_Zero/{sha}/compiler/COMPILER_PIPELINE.json"
            ir.compiler_identity.remote_commit_sha = sha
        else:
            url_context = "https://raw.githubusercontent.com/mKouko-T/Foundation_Zero/main/BOOT_CONTEXT.md"
            url_order = "https://raw.githubusercontent.com/mKouko-T/Foundation_Zero/main/compiler/COMPILER_PIPELINE.json"
            try:
                api_url = "https://api.github.com/repos/mKouko-T/Foundation_Zero/commits/main"
                req_api = urllib.request.Request(api_url, headers={"User-Agent": "Foundation-Zero-Compiler"})
                with urllib.request.urlopen(req_api) as res:
                    ir.compiler_identity.remote_commit_sha = json.loads(res.read().decode('utf-8')).get("sha", "UNKNOWN")
            except Exception:
                pass

        try:
            req_context = urllib.request.Request(url_context)
            with urllib.request.urlopen(req_context) as res:
                ir.raw_files["boot_context"] = self._canonicalize(res.read())
            
            req_order = urllib.request.Request(url_order)
            with urllib.request.urlopen(req_order) as res:
                ir.pipeline_graph = json.loads(res.read().decode('utf-8'))
        except Exception as e:
            raise RuntimeError(f"COMPILER FATAL: Could not fetch remote compiler specs. {e}")

    def _read_pipeline_artifacts(self, ir: CanonicalIR):
        """Reads local artifacts declared in the pipeline graph into IR."""
        for stage in ir.pipeline_graph.get("stages", []):
            stage_id = stage["id"]
            filepath = stage["artifact"]
            
            # Skip remote stage since we fetch it separately above.
            if "(remote)" in filepath:
                continue 
            
            full_path = self.root_dir / filepath
            if not full_path.exists():
                raise RuntimeError(f"MISSING FILE FATAL: {filepath} is required for compilation.")
                
            ir.raw_files[stage_id] = self._canonicalize(full_path.read_bytes())

    def _parse_semantic_fields(self, ir: CanonicalIR):
        """Maps canonicalized raw bytes into structured knowledge models."""
        ir.knowledge_state.runtime_rules = ir.raw_files.get("runtime_contract", "")
        ir.knowledge_state.canonical_model = ir.raw_files.get("canonical_model", "")
        ir.knowledge_state.methodology = ir.raw_files.get("genesis_methodology", "")
        ir.execution_context.task_state = ir.raw_files.get("task_state", "")
        
        boot_content = ir.raw_files.get("bootstrap", "")
        mission_match = re.search(r"## Mission\n(.*?)\n##", boot_content, re.DOTALL)
        if mission_match:
            ir.execution_context.mission = mission_match.group(1).strip()
            
        phase_match = re.search(r"## Current Phase\n(.*?)\n##", boot_content, re.DOTALL)
        if phase_match:
            ir.execution_context.phase = phase_match.group(1).strip()
            
        constraints_match = re.search(r"## Active Constraints\n(.*?)\n##", boot_content, re.DOTALL)
        if constraints_match:
            ir.execution_context.constraints = [
                line.strip("- ").strip() for line in constraints_match.group(1).split("\n") if line.strip()
            ]

    def _fetch_local_git_sha(self, ir: CanonicalIR):
        import subprocess
        try:
            result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(self.root_dir), capture_output=True, text=True, check=True)
            ir.repository_identity.commit_sha = result.stdout.strip()
            
            status = subprocess.run(["git", "status", "--porcelain"], cwd=str(self.root_dir), capture_output=True, text=True, check=True)
            if status.stdout.strip():
                ir.repository_identity.commit_sha = "DIRTY"
        except Exception:
            ir.repository_identity.commit_sha = "UNKNOWN"
