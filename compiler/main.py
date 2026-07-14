import sys
from pathlib import Path

# Add the parent directory to sys.path so we can import 'compiler' as a module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from compiler.ir import CanonicalIR
from compiler.parser import Parser
from compiler.validator import Validator
from compiler.manifest import ManifestGenerator
from compiler.emitter import Emitter

def compile_boot_package(root_dir: str = "."):
    print("Foundation Zero Compiler - v1.0")
    print("================================")
    
    ir = CanonicalIR()
    
    try:
        print("[Pass 1 & 2] Source Discovery & Parsing...")
        parser = Parser(root_dir)
        parser.parse(ir)
        
        print("[Pass 3, 4, 5] Hash Generation, Dependency Resolution & Validation...")
        validator = Validator(root_dir)
        validator.validate(ir)
    except Exception as e:
        print(f"\nCOMPILATION FAILED: {e}")
        sys.exit(1)
        
    print("[Pass 6 & 7] Certification & Manifest Generation...")
    manifest_gen = ManifestGenerator(root_dir)
    manifest_gen.generate(ir)
    
    print("[Pass 8] Emission...")
    emitter = Emitter(root_dir)
    emitter.emit(ir)
    
    print(f"\nCOMPILATION SUCCESSFUL.")
    print(f"Conforms to Foundation Zero Compiler Specification v1.0")
    print(f"BOOT_ID: {ir.provenance.boot_id}")
    print(f"Artifacts: BOOT_MANIFEST.json, BOOT_PACKAGE.md")

if __name__ == "__main__":
    import argparse
    arg_parser = argparse.ArgumentParser(description="Compile the Foundation Zero BOOT_PACKAGE.")
    arg_parser.add_argument("--root", default=".", help="Root directory of the Cornerstone repository.")
    args = arg_parser.parse_args()
    
    compile_boot_package(args.root)
