import os
from pathlib import Path
from compiler.ir import CanonicalIR

class Emitter:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)

    def emit(self, ir: CanonicalIR):
        """Pass 8: Emission. Generates the deterministic BOOT_PACKAGE.md for the runtime."""
        
        lines = []
        
        # Header (Deterministic, no timestamps)
        lines.append("# BOOT_PACKAGE")
        lines.append(f"**BOOT_ID:** `{ir.boot_id}`")
        lines.append(f"**Compiler:** {ir.compiler_identity.name} {ir.compiler_identity.version}")
        lines.append(f"**Repository:** {ir.repository_identity.name} ({ir.repository_identity.branch})")
        lines.append("")
        
        # Section 1: Verified Compiler
        lines.append("=========================")
        lines.append("## SECTION 1: Verified Compiler")
        lines.append(f"*(Remote Source: {ir.compiler_identity.source_repository})*")
        lines.append("")
        lines.append(ir.compiler_identity.content)
        lines.append("")
        
        # Section 2: Runtime Rules
        lines.append("=========================")
        lines.append("## SECTION 2: Runtime Rules")
        lines.append("")
        lines.append(ir.runtime_rules)
        lines.append("")
        
        # Section 3: Project Identity & Constraints
        lines.append("=========================")
        lines.append("## SECTION 3: Project Identity")
        lines.append(f"**Mission:** {ir.execution_context.mission}")
        lines.append(f"**Phase:** {ir.execution_context.phase}")
        lines.append("**Active Constraints:**")
        for constraint in ir.execution_context.constraints:
            lines.append(f"- {constraint}")
        lines.append("")
        
        # Section 4: Canonical Model
        lines.append("=========================")
        lines.append("## SECTION 4: Canonical Model")
        lines.append("")
        lines.append(ir.canonical_model)
        lines.append("")
        
        # Section 5: Genesis Methodology
        lines.append("=========================")
        lines.append("## SECTION 5: Genesis Methodology")
        lines.append("")
        lines.append(ir.methodology)
        lines.append("")
        
        # Section 6: Execution State
        lines.append("=========================")
        lines.append("## SECTION 6: Current Task State")
        lines.append("")
        lines.append(ir.execution_context.task_state)
        lines.append("")
        
        # Final Verification Instruction
        lines.append("=========================")
        lines.append("## INSTRUCTION TO RUNTIME")
        lines.append("1. Verify the `BOOT_ID` in this package matches the `boot_id` in `BOOT_MANIFEST.json`.")
        lines.append("2. Verify the Certification flags in `BOOT_MANIFEST.json` are PASS.")
        lines.append("3. If verified, declare **BOOT COMPLETE** and proceed autonomously.")
        
        package_content = "\n".join(lines)
        
        # Write to file
        package_path = self.root_dir / "BOOT_PACKAGE.md"
        package_path.write_text(package_content, encoding="utf-8")
