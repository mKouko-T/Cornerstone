import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from compiler.ir import CanonicalIR

class ManifestGenerator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)

    def generate(self, ir: CanonicalIR):
        """Pass 6 & 7: Manifest Generation and Certification."""
        
        # 1. Build the base manifest structure
        manifest = {
            "schema": "v1",
            "compiler": {
                "name": ir.compiler_identity.name,
                "version": ir.compiler_identity.version,
                "remote_commit_sha": ir.compiler_identity.remote_commit_sha,
                "source_repository": ir.compiler_identity.source_repository,
                "guarantees": ir.compiler_identity.guarantees
            },
            "repository": {
                "name": ir.repository_identity.name,
                "branch": ir.repository_identity.branch,
                "commit_sha": ir.repository_identity.commit_sha
            },
            "dependencies": ir.dependency_graph,
            "provenance": ir.file_hashes
        }
        
        # 2. Serialize and hash the base manifest
        manifest_json = json.dumps(manifest, indent=2, sort_keys=True)
        ir.manifest_hash = hashlib.sha256(manifest_json.encode('utf-8')).hexdigest()
        
        # 3. Generate Cryptographic-ready BOOT_ID
        boot_id_payload = (
            ir.compiler_identity.version + 
            ir.compiler_identity.remote_commit_sha + 
            manifest_json + 
            ir.repository_identity.commit_sha
        )
        ir.boot_id = hashlib.sha256(boot_id_payload.encode('utf-8')).hexdigest()
        
        # 4. Certification (derived from IR and Manifest)
        certification = {
            "compiler_identity": f"{ir.compiler_identity.name} {ir.compiler_identity.version}",
            "repository_commit": ir.repository_identity.commit_sha,
            "manifest_hash": ir.manifest_hash,
            "boot_id": ir.boot_id,
            "compiler_signature": ir.compiler_identity.signature
        }
        
        # 5. Append Certification to Manifest and save
        manifest["certification"] = certification
        final_manifest_json = json.dumps(manifest, indent=2, sort_keys=True)
        
        manifest_path = self.root_dir / "BOOT_MANIFEST.json"
        manifest_path.write_text(final_manifest_json, encoding="utf-8")
