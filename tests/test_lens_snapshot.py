import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "dl-vibe-lens-skill" / "scripts" / "lens_snapshot.py"

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
        self.assertIn("## 问题池", text)
        self.assertIn("## 当前工作", text)
        self.assertIn("## 迭代记录", text)
        self.assertIn("不要改名", text)
        self.assertIn("不替你排优先级", text)

    def test_init_creates_settings_and_chinese_record_by_default(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--project-root", str(self.tmp), "--init"],
            text=True,
            capture_output=True,
            check=False,
        )

        record = self.tmp / "docs" / "iteration-record.md"
        settings = self.tmp / "docs" / "vibe-lens-settings.json"

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(record.exists())
        self.assertTrue(settings.exists())
        text = record.read_text(encoding="utf-8")
        config = json.loads(settings.read_text(encoding="utf-8"))
        self.assertIn("# Vibe Lens 记录", text)
        self.assertIn("## 问题池", text)
        self.assertIn("## 当前工作", text)
        self.assertIn("## 迭代记录", text)
        self.assertEqual(config["reply_entry_mode"], "always")
        self.assertEqual(config["record_language"], "auto")

    def test_init_can_create_english_record_when_requested(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--project-root",
                str(self.tmp),
                "--init",
                "--record-language",
                "en",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        record = self.tmp / "docs" / "iteration-record.md"
        self.assertEqual(result.returncode, 0, result.stderr)
        text = record.read_text(encoding="utf-8")
        self.assertIn("# Vibe Lens Record", text)
        self.assertIn("## Issue Pool", text)
        self.assertIn("## Active Work", text)
        self.assertIn("## Iteration Log", text)

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
        self.assertIn("Iteration Path", html)
        self.assertIn("Render visual sandbox", html)

    def test_html_report_contains_confirmed_lens_interface(self):
        self.write_record(
            """# Vibe Lens Record

## Issue Pool
| ID | Issue | Source | Status | Evidence | Related Files |
|---|---|---|---|---|---|
| VL-001 | Keep the homepage compact | operator | open | User wants a stable board layout | README.md |
| VL-002 | Show code diff with visual rings | operator | resolved | Git diff data exists | vibe-lens/scripts/lens_snapshot.py |

## Active Work
| Session | Task | Files Or Areas | Status | Notes |
|---|---|---|---|---|
| chat-a | Report template | vibe-lens/assets/report_template.html | in progress | Current UI work |

## Iteration Log
### 2026-07-03: Confirm homepage gateways
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        output = self.tmp / "lens-report.html"
        lens_snapshot.write_html_report(snapshot, output)

        html = output.read_text(encoding="utf-8")
        self.assertIn('lang="zh-CN"', html)
        self.assertIn("当前问题 / 任务", html)
        self.assertIn("代码差异", html)
        self.assertIn("沙盘演示", html)
        self.assertIn("迭代路径", html)
        self.assertIn('id="current-detail"', html)
        self.assertIn('id="history-detail"', html)
        self.assertIn('id="files-detail"', html)
        self.assertIn('id="code-detail"', html)
        self.assertIn('id="sandbox-detail"', html)
        self.assertIn('id="path-detail"', html)
        self.assertIn('["openQuestions", data.open_question_count, "current-detail"]', html)
        self.assertIn('["totalQuestions", data.issue_count, "history-detail"]', html)
        self.assertIn('["changedFiles", diff.changed_file_count || 0, "files-detail"]', html)
        self.assertIn('["codeChange", `+${diff.total_added || 0} / -${diff.total_deleted || 0}`, "code-detail"]', html)
        self.assertIn("阶段刻度，不是日期", html)
        self.assertIn("对话入口设置", html)
        self.assertIn("打开 Vibe Lens", html)
        self.assertIn("diff-card", html)
        self.assertIn("diff-body", html)
        self.assertIn("diff-file-list", html)
        self.assertIn("reply_entry_mode", html)
        self.assertIn("默认每轮回复末尾显示入口", html)
        self.assertIn('data-entry-mode="always"', html)
        self.assertIn('data-entry-mode="when_used"', html)
        self.assertIn('data-entry-mode="off"', html)
        self.assertIn("持久行为以项目设置文件或明确提示词为准", html)
        self.assertIn("settings.contains(event.target)", html)
        self.assertIn("settings.classList.remove(\"open\")", html)

    def test_skill_metadata_and_docs_use_dl_trigger(self):
        skill_md = (ROOT / "dl-vibe-lens-skill" / "SKILL.md").read_text(encoding="utf-8")
        openai_yaml = (ROOT / "dl-vibe-lens-skill" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("name: dl-vibe-lens-skill", skill_md)
        self.assertIn("$dl-vibe-lens-skill", openai_yaml)
        self.assertIn("dl-vibe-lens-skill/", readme)
        self.assertIn("$dl-vibe-lens-skill", readme)
        self.assertNotIn("$vibe-lens", readme)
        self.assertNotIn(".codex\\skills\\vibe-lens", readme)

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

    def test_snapshot_builds_visual_cognition_signals(self):
        self.write_record(
            """# Vibe Lens 记录

## 问题池
| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 | 验证 | 解释状态 |
|---|---|---|---|---|---|---|---|
| VL-101 | 总览详情入口混乱 | operator | open | 用户指出四个指标跳到同一详情页 | dl-vibe-lens-skill/assets/report_template.html | python -m unittest tests.test_lens_snapshot | 已解释 |
| VL-102 | 路径图还是演示图 | operator | open | 用户指出路径图落地残缺 | dl-vibe-lens-skill/assets/report_template.html |  | 解释不足 |
| VL-103 | 解释状态要更严格 | operator | open | 需要确认未知值不会被当成已解释 | dl-vibe-lens-skill/scripts/lens_snapshot.py |  | 待解释 |

## 当前工作
| 会话 | 任务 | 涉及文件 | 状态 | 备注 |
|---|---|---|---|---|
| 2026-07-09 | 设计可视化认知层 | docs/ | discussing | 计划阶段 |

## 迭代记录
### 2026-07-09: 设计可视化认知层
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        first = snapshot["open_questions"][0]["__lens"]
        second = snapshot["open_questions"][1]["__lens"]
        third = snapshot["open_questions"][2]["__lens"]

        self.assertEqual(first["evidence"]["complete"], 3)
        self.assertEqual(first["evidence"]["total"], 3)
        self.assertEqual(first["evidence"]["percent"], 100)
        self.assertEqual(first["verification"]["percent"], 100)
        self.assertEqual(first["explanation"]["label"], "已解释")
        self.assertEqual(first["overall_percent"], 100)

        self.assertEqual(second["verification"]["percent"], 0)
        self.assertIn("验证", second["verification"]["missing"])
        self.assertEqual(second["explanation"]["label"], "解释不足")
        self.assertLess(second["overall_percent"], 100)

        self.assertEqual(third["explanation"]["label"], "待解释")
        self.assertEqual(third["explanation"]["complete"], 0)
        self.assertEqual(third["explanation"]["percent"], 0)
        self.assertIn("解释", third["explanation"]["missing"])
        self.assertLess(third["overall_percent"], 100)

        self.assertEqual(snapshot["cognition_summary"]["issues_with_evidence"], 3)
        self.assertEqual(snapshot["cognition_summary"]["issues_with_verification"], 1)
        self.assertEqual(snapshot["cognition_summary"]["issues_with_full_explanation"], 1)

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
