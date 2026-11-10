from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts.compile_figures import compile_figures


class CompileFiguresTests(unittest.TestCase):
    def test_recursive_paths_with_spaces_and_duplicate_basenames(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = [root / "search" / "flow.tikz", root / "sort" / "deep folder" / "flow.tikz"]
            for source in sources:
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text("test", encoding="utf-8")
            (root / "unrelated.txt").write_text("test", encoding="utf-8")
            with patch("scripts.compile_figures.shutil.which", return_value="/bin/tikzc"), patch(
                "scripts.compile_figures.subprocess.run"
            ) as run:
                self.assertEqual(compile_figures(root), 2)
            self.assertEqual(run.call_count, 2)
            for call, source in zip(run.call_args_list, sources):
                self.assertEqual(
                    call.args[0],
                    ["/bin/tikzc", str(source), "--format", "svg", "--output", str(source.with_suffix(".svg"))],
                )
                self.assertEqual(call.kwargs, {"cwd": source.parent, "check": True})

    def test_empty_directory_needs_no_compiler(self):
        with tempfile.TemporaryDirectory() as directory, patch(
            "scripts.compile_figures.shutil.which"
        ) as which:
            self.assertEqual(compile_figures(Path(directory)), 0)
            which.assert_not_called()

    def test_missing_compiler_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "flow.tikz").touch()
            with patch("scripts.compile_figures.shutil.which", return_value=None):
                with self.assertRaisesRegex(RuntimeError, "not on PATH"):
                    compile_figures(root)

    def test_compiler_failure_stops_the_build(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.tikz").touch()
            (root / "b.tikz").touch()
            with patch("scripts.compile_figures.shutil.which", return_value="/bin/tikzc"), patch(
                "scripts.compile_figures.subprocess.run",
                side_effect=subprocess.CalledProcessError(3, "tikzc"),
            ) as run:
                with self.assertRaises(subprocess.CalledProcessError):
                    compile_figures(root)
                self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
