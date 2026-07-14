import os
import shutil
import json
import pytest
import subprocess
from pathlib import Path

# We will test using pytest

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

COMPILER_MAIN = Path(__file__).parent / "compiler" / "main.py"

def test_1_determinism_crlf_vs_lf(tmp_path):
    repo_a = setup_mock_repo(tmp_path / "repo_a")
    repo_b = setup_mock_repo(tmp_path / "repo_b")
    
    # Variant A: CRLF
    for p in repo_a.rglob("*.md"):
        content = p.read_text(encoding='utf-8')
        p.write_bytes(content.replace('\n', '\r\n').encode('utf-8'))
        
    # Variant B: LF
    for p in repo_b.rglob("*.md"):
        content = p.read_text(encoding='utf-8')
        p.write_bytes(content.replace('\r\n', '\n').encode('utf-8'))
        
    subprocess.run(["python", str(COMPILER_MAIN), "--root", "."], cwd=str(repo_a), check=True)
    subprocess.run(["python", str(COMPILER_MAIN), "--root", "."], cwd=str(repo_b), check=True)
    
    man_a = get_manifest(repo_a)
    man_b = get_manifest(repo_b)
    
    assert man_a['certification']['boot_id'] == man_b['certification']['boot_id']

def test_2_unicode_normalization(tmp_path):
    repo_a = setup_mock_repo(tmp_path / "repo_nfc")
    repo_b = setup_mock_repo(tmp_path / "repo_nfd")
    
    # NFC
    (repo_a / "docs/Canonical_Model.md").write_text("Caf\u00e9", encoding='utf-8')
    # NFD
    (repo_b / "docs/Canonical_Model.md").write_text("Cafe\u0301", encoding='utf-8')
    
    subprocess.run(["python", str(COMPILER_MAIN), "--root", "."], cwd=str(repo_a), check=True)
    subprocess.run(["python", str(COMPILER_MAIN), "--root", "."], cwd=str(repo_b), check=True)
    
    assert get_manifest(repo_a)['certification']['boot_id'] == get_manifest(repo_b)['certification']['boot_id']

def test_3_bom_stripping(tmp_path):
    repo_a = setup_mock_repo(tmp_path / "repo_bom")
    repo_b = setup_mock_repo(tmp_path / "repo_nobom")
    
    # Add BOM to A
    content = (repo_a / "BOOTSTRAP.md").read_bytes()
    (repo_a / "BOOTSTRAP.md").write_bytes(b'\xef\xbb\xbf' + content)
    
    subprocess.run(["python", str(COMPILER_MAIN), "--root", "."], cwd=str(repo_a), check=True)
    subprocess.run(["python", str(COMPILER_MAIN), "--root", "."], cwd=str(repo_b), check=True)
    
    assert get_manifest(repo_a)['certification']['boot_id'] == get_manifest(repo_b)['certification']['boot_id']

def test_5_missing_dependency(tmp_path):
    repo = setup_mock_repo(tmp_path / "repo_miss")
    (repo / "docs/Canonical_Model.md").unlink()
    
    res = subprocess.run(["python", str(COMPILER_MAIN), "--root", "."], cwd=str(repo), capture_output=True, text=True)
    assert res.returncode != 0
    assert "MISSING FILE FATAL" in res.stdout

def test_6_ambiguity_rejection(tmp_path):
    repo = setup_mock_repo(tmp_path / "repo_amb")
    (repo / "docs/Canonical_Model_v2.md").write_text("Ambiguous", encoding='utf-8')
    
    res = subprocess.run(["python", str(COMPILER_MAIN), "--root", "."], cwd=str(repo), capture_output=True, text=True)
    assert res.returncode != 0
    assert "AMBIGUITY FATAL" in res.stdout

def test_7_pinned_mode(tmp_path):
    repo = setup_mock_repo(tmp_path / "repo_pinned")
    env = os.environ.copy()
    env["COMPILER_MODE"] = "pinned"
    env["PINNED_COMMIT_SHA"] = "141b01e7f98a6a4022a9e259dc3f447dbd9f3b25" # From previous push
    
    subprocess.run(["python", str(COMPILER_MAIN), "--root", "."], cwd=str(repo), env=env, check=True)
    man = get_manifest(repo)
    assert man['compiler']['remote_commit_sha'] == "141b01e7f98a6a4022a9e259dc3f447dbd9f3b25"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
