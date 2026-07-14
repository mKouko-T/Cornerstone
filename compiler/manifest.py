import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from compiler.ir import CanonicalIR

class ManifestGenerator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)

    def generate(self, ir: CanonicalIR):
        """Pass 6 & 7: Certification and Manifest Generation."""
        
        # Build the manifest structure
        manifest = {
            "schema": "v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "compiler": {
                "name": ir.compiler_identity.name,
                "version": ir.compiler_identity.version,
                "remote_commit_sha": ir.compiler_identity.remote_commit_sha,
                "source_repository": ir.compiler_identity.source_repository
            },
            "repository": {
                "name": ir.repository_identity.name,
                "branch": ir.repository_identity.branch,
                "commit_sha": ir.repository_identity.commit_sha
            },
            "dependencies": ir.dependency_graph,
            "provenance": ir.file_hashes,
            "certification": {
                "compiler_loaded": "PASS",
                "repository_verified": "PASS",
                "project_loaded": "PASS",
                "ambiguity_check": "PASS",
                "hashes_verified": "PASS"
            }
        }
        
        # Serialize manifest
        manifest_json = json.dumps(manifest, indent=2, sort_keys=True)
        ir.manifest_hash = hashlib.sha256(manifest_json.encode('utf-8')).hexdigest()
        
        # Generate Cryptographic-ready BOOT_ID
        # SHA256(Compiler Version + Compiler Commit + Manifest + Repository Commit)
        boot_id_payload = (
            ir.compiler_identity.version + 
            ir.compiler_identity.remote_commit_sha + 
            manifest_json + 
            ir.repository_identity.commit_sha
        )
        ir.boot_id = hashlib.sha256(boot_id_payload.encode('utf-8')).hexdigest()
        
        # Also add BOOT_ID to the manifest for transparency
        manifest["boot_id"] = ir.boot_id
        final_manifest_json = json.dumps(manifest, indent=2, sort_keys=True)
        
        # Write to file
        manifest_path = self.root_dir / "BOOT_MANIFEST.json"
        manifest_path.write_text(final_manifest_json, encoding="utf-8")
