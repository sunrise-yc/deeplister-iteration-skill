import importlib.util
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "vibe-lens" / "scripts" / "lens_snapshot.py"

spec = importlib.util.spec_from_file_location("lens_snapshot", SCRIPT)
lens_snapshot = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(lens_snapshot)


class LensSnapshotTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, onerror=self.remove_readonly)

    @staticmethod
    def remove_readonly(func, path, _exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def write_record(self, text: str) -> Path:
        docs = self.tmp / "docs"
        docs.mkdir(exist_ok=True)
        record = docs / "iteration-record.md"
        record.write_text(text, encoding="utf-8")
        return record

    def test_reads_record_as_neutral_question_display(self):
        self.write_record(
            """# Vibe Lens Record

## Issue Pool
| ID | Issue | Impact | Priority | Status | Next Step |
|---|---|---|---|---|---|
| VL-001 | Show current questions | Agent and operator need a shared view | P0 | open | Display without ranking |
| VL-002 | Keep setup automatic | New users should not create files by hand | P1 | done | Covered by init |

## Active Work
| Session | Task | Files Or Areas | Status | Notes |
|---|---|---|---|---|
| 2026-07-02 | Build lens report | vibe-lens/ | in progress | Current session |

## Follow-up Flow Notes
| Scenario | Current Behavior | Issue | Improvement |
|---|---|---|---|
| Parallel chats | Context can drift | Conflicts are likely | Show touched areas |

## Iteration Log
### 2026-07-02: Reposition as review sandbox
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)

        self.assertEqual(snapshot["issue_count"], 2)
        self.assertEqual(snapshot["open_question_count"], 1)
        self.assertNotIn("recommended_next", snapshot)
        self.assertEqual(snapshot["open_questions"][0]["ID"], "VL-001")
        self.assertEqual(snapshot["active_work_count"], 1)
        self.assertEqual(snapshot["latest_iteration"], "2026-07-02: Reposition as review sandbox")

    def test_collects_git_diff_stats_without_ai_guessing(self):
        self.write_record(
            """# Vibe Lens Record

## Issue Pool
| ID | Issue | Impact | Priority | Status | Next Step |
|---|---|---|---|---|---|
| VL-001 | Show diff stats | Review needs code change evidence | P0 | open | Read Git numstat |

## Iteration Log
### 2026-07-02: Diff stats
"""
        )
        self.run_git("init")
        self.run_git("config", "user.email", "test@example.com")
        self.run_git("config", "user.name", "Test User")
        (self.tmp / "app.py").write_text("one\ntwo\n", encoding="utf-8")
        self.run_git("add", "app.py", "docs/iteration-record.md")
        self.run_git("commit", "-m", "initial")
        (self.tmp / "app.py").write_text("one\nthree\nfour\n", encoding="utf-8")
        (self.tmp / "notes.md").write_text("new\n", encoding="utf-8")

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        diff = snapshot["git_diff"]

        self.assertEqual(diff["total_added"], 2)
        self.assertEqual(diff["total_deleted"], 1)
        self.assertEqual(diff["changed_file_count"], 1)
        self.assertEqual(diff["files"][0]["path"], "app.py")
        self.assertEqual(diff["untracked_files"], ["notes.md"])

    def test_init_creates_lens_record_without_manual_file_setup(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--project-root", str(self.tmp), "--init"],
            text=True,
            capture_output=True,
            check=False,
        )

        record = self.tmp / "docs" / "iteration-record.md"
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(record.exists())
        text = record.read_text(encoding="utf-8")
        self.assertIn("## Issue Pool", text)
        self.assertIn("## Active Work", text)
        self.assertIn("## Iteration Log", text)
        self.assertIn("Do not rename these headings", text)
        self.assertIn("Do not rank issues", text)

    def test_generates_static_html_report(self):
        self.write_record(
            """# Vibe Lens Record

## Issue Pool
| ID | Issue | Impact | Priority | Status | Next Step |
|---|---|---|---|---|---|
| VL-001 | Render visual sandbox | Markdown alone is not enough | P0 | open | Generate HTML |

## Iteration Log
### 2026-07-02: HTML report
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        output = self.tmp / "lens-report.html"
        lens_snapshot.write_html_report(snapshot, output)

        html = output.read_text(encoding="utf-8")
        self.assertIn("Vibe Lens", html)
        self.assertIn("Current Questions", html)
        self.assertIn("Code Diff", html)
        self.assertIn("Iteration Direction", html)
        self.assertIn("Render visual sandbox", html)

    def test_falls_back_to_legacy_chinese_iteration_record(self):
        docs = self.tmp / "docs"
        docs.mkdir()
        (docs / "迭代记录.md").write_text(
            """# DeepLister 迭代记录

## 问题池
| 编号 | 问题 | 影响 | 优先级 | 状态 | 下一步 |
|---|---|---|---|---|---|
| DL-001 | 旧文档仍然可读 | 已有用户不能断 | P0 | 待处理 | 保留兼容 |

## 追问流程专项记录
| 场景 | 当前表现 | 问题 | 优化方向 |
|---|---|---|---|
| 旧标题 | 能解析 | 兼容风险 | 保留别名 |

## 迭代记录
### 2026-07-01：旧文档兼容
""",
            encoding="utf-8",
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)

        self.assertEqual(snapshot["record"], str(docs / "迭代记录.md"))
        self.assertEqual(snapshot["open_questions"][0]["编号"], "DL-001")
        self.assertEqual(snapshot["latest_iteration"], "2026-07-01：旧文档兼容")
        self.assertEqual(snapshot["follow_up_case_count"], 1)

    def run_git(self, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=self.tmp,
            text=True,
            capture_output=True,
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
