import os
import shutil
import json
import pytest
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

# We will test using pytest

@pytest.fixture(autouse=True)
def mock_remote_specs():
    with patch("urllib.request.urlopen") as mock_urlopen:
        def side_effect(req):
            url = req.full_url if hasattr(req, 'full_url') else req
            mock_res = MagicMock()
            if "api.github.com" in url:
                mock_res.read.return_value = json.dumps({"sha": "mocked_sha"}).encode('utf-8')
            elif "BOOT_CONTEXT.md" in url:
                mock_res.read.return_value = b"Foundation Zero Lite v1.0\nMock Context"
            elif "COMPILER_PIPELINE.json" in url:
                pipeline = {
                    "schema_version": "1.0",
                    "spec_version": "1.0",
                    "pipeline_id": "test_boot",
                    "capabilities": ["topological_pipeline"],
                    "stages": [
                        {"id": "boot_protocol", "artifact": "CRBP.md", "depends_on": []},
                        {"id": "boot_context", "artifact": "Foundation_Zero/BOOT_CONTEXT.md (remote)", "depends_on": []},
                        {"id": "runtime_contract", "artifact": "docs/Runtime_Contract.md", "depends_on": ["boot_protocol", "boot_context"]},
                        {"id": "bootstrap", "artifact": "BOOTSTRAP.md", "depends_on": ["runtime_contract"]},
                        {"id": "canonical_model", "artifact": "docs/Canonical_Model.md", "depends_on": ["runtime_contract"]},
                        {"id": "genesis_methodology", "artifact": "docs/Genesis_Methodology.md", "depends_on": ["runtime_contract"]},
                        {"id": "task_state", "artifact": "task.md", "depends_on": ["bootstrap", "canonical_model", "genesis_methodology"]}
                    ]
                }
                mock_res.read.return_value = json.dumps(pipeline).encode('utf-8')
            else:
                mock_res.read.return_value = b""
            mock_res.__enter__.return_value = mock_res
            return mock_res
        
        mock_urlopen.side_effect = side_effect
        yield

def setup_mock_repo(base_dir: Path):
    if base_dir.exists():
        shutil.rmtree(base_dir)
    base_dir.mkdir(parents=True)
    
    (base_dir / "docs").mkdir()
    
    # Write standard required files
    files = {
        "CRBP.md": "CRBP Content",
        "BOOTSTRAP.md": "## Mission\nTest Mission\n##\n## Current Phase\nTest Phase\n##\n## Active Constraints\n- Constraint 1\n##",
        "docs/Runtime_Contract.md": "Runtime Rules",
        "docs/Canonical_Model.md": "Canonical Model",
        "docs/Genesis_Methodology.md": "Methodology",
        "task.md": "Task State"
    }
    for filepath, content in files.items():
        (base_dir / filepath).write_text(content, encoding='utf-8')
        
    return base_dir

def get_manifest(base_dir: Path):
    return json.loads((base_dir / "BOOT_MANIFEST.json").read_text(encoding='utf-8'))

from compiler.main import compile_boot_package

def run_compiler(root_dir: str):
    compile_boot_package(root_dir)

def test_1_determinism_crlf_vs_lf(tmp_path):
    repo_a = setup_mock_repo(tmp_path / "repo_a")
    repo_b = setup_mock_repo(tmp_path / "repo_b")
    
    for p in repo_a.rglob("*.md"):
        content = p.read_text(encoding='utf-8')
        p.write_bytes(content.replace('\n', '\r\n').encode('utf-8'))
        
    for p in repo_b.rglob("*.md"):
        content = p.read_text(encoding='utf-8')
        p.write_bytes(content.replace('\r\n', '\n').encode('utf-8'))
        
    run_compiler(str(repo_a))
    run_compiler(str(repo_b))
    
    man_a = get_manifest(repo_a)
    man_b = get_manifest(repo_b)
    
    assert man_a['certification']['boot_id'] == man_b['certification']['boot_id']

def test_2_unicode_normalization(tmp_path):
    repo_a = setup_mock_repo(tmp_path / "repo_nfc")
    repo_b = setup_mock_repo(tmp_path / "repo_nfd")
    
    (repo_a / "docs/Canonical_Model.md").write_text("Caf\u00e9", encoding='utf-8')
    (repo_b / "docs/Canonical_Model.md").write_text("Cafe\u0301", encoding='utf-8')
    
    run_compiler(str(repo_a))
    run_compiler(str(repo_b))
    
    assert get_manifest(repo_a)['certification']['boot_id'] == get_manifest(repo_b)['certification']['boot_id']

def test_3_bom_stripping(tmp_path):
    repo_a = setup_mock_repo(tmp_path / "repo_bom")
    repo_b = setup_mock_repo(tmp_path / "repo_nobom")
    
    content = (repo_a / "BOOTSTRAP.md").read_bytes()
    (repo_a / "BOOTSTRAP.md").write_bytes(b'\xef\xbb\xbf' + content)
    
    run_compiler(str(repo_a))
    run_compiler(str(repo_b))
    
    assert get_manifest(repo_a)['certification']['boot_id'] == get_manifest(repo_b)['certification']['boot_id']

def test_5_missing_dependency(tmp_path, capsys):
    repo = setup_mock_repo(tmp_path / "repo_miss")
    (repo / "docs/Canonical_Model.md").unlink()
    
    with pytest.raises(SystemExit):
        run_compiler(str(repo))
    
    captured = capsys.readouterr()
    assert "MISSING FILE FATAL" in captured.out

def test_7_pinned_mode(tmp_path, monkeypatch):
    repo = setup_mock_repo(tmp_path / "repo_pinned")
    monkeypatch.setenv("COMPILER_MODE", "pinned")
    monkeypatch.setenv("PINNED_COMMIT_SHA", "141b01e7f98a6a4022a9e259dc3f447dbd9f3b25")
    
    run_compiler(str(repo))
    man = get_manifest(repo)
    assert man['compiler']['remote_commit_sha'] == "141b01e7f98a6a4022a9e259dc3f447dbd9f3b25"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
