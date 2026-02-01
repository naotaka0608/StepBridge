
import sys
from pathlib import Path

# Add src to python path to prefer local source over installed package
root_dir = Path(__file__).parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))

print(f"DEBUG: Running from source: {src_dir}")

from step_to_obj.main import run_app

if __name__ == "__main__":
    run_app()
