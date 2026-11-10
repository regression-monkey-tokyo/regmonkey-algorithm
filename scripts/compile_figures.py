"""Compile every figures/**/*.tikz file to a neighboring SVG using tikzc."""

from pathlib import Path
import shutil
import subprocess
import sys


def compile_figures(root: Path) -> int:
    sources = sorted(root.resolve().rglob("*.tikz"))
    if not sources:
        print(f"No .tikz files in {root}; skipping figure compilation.")
        return 0

    compiler = shutil.which("tikzc")
    if compiler is None:
        raise RuntimeError("tikzc is not on PATH; see the Cargo install command in README.md")

    for source in sources:
        output = source.with_suffix(".svg")
        print(f"Compiling {source.relative_to(root.resolve())}", flush=True)
        subprocess.run(
            [compiler, str(source), "--format", "svg", "--output", str(output)],
            cwd=source.parent,
            check=True,
        )

    print(f"Compiled {len(sources)} figure(s).")
    return len(sources)


if __name__ == "__main__":
    try:
        compile_figures(Path(__file__).resolve().parents[1] / "figures")
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"Figure compilation failed: {error}", file=sys.stderr)
        sys.exit(1)
