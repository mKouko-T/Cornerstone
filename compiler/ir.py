from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class CompilerIdentity:
    name: str = "Foundation Zero Lite"
    version: str = "v1.0"
    remote_commit_sha: str = ""
    hash_sha256: str = ""
    source_repository: str = "mKouko-T/Foundation_Zero"
    signature: str = "UNSIGNED"
    guarantees: List[str] = field(default_factory=list)
    content: str = ""

@dataclass
class RepositoryIdentity:
    name: str = "Cornerstone"
    branch: str = "main"
    commit_sha: str = ""

@dataclass
class ExecutionContext:
    mission: str = ""
    phase: str = ""
    constraints: List[str] = field(default_factory=list)
    task_state: str = ""

@dataclass
class KnowledgeState:
    runtime_rules: str = ""
    canonical_model: str = ""
    methodology: str = ""

@dataclass
class Provenance:
    dependency_graph: List[str] = field(default_factory=list)
    file_hashes: Dict[str, str] = field(default_factory=dict)
    manifest_hash: str = ""
    boot_id: str = ""

@dataclass
class CanonicalIR:
    """The central architectural abstraction of Foundation Zero.
    Everything revolves around the IR—not the Markdown.
    """
    compiler_identity: CompilerIdentity = field(default_factory=CompilerIdentity)
    repository_identity: RepositoryIdentity = field(default_factory=RepositoryIdentity)
    execution_context: ExecutionContext = field(default_factory=ExecutionContext)
    knowledge_state: KnowledgeState = field(default_factory=KnowledgeState)
    provenance: Provenance = field(default_factory=Provenance)
