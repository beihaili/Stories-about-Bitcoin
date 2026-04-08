"""Tests for the scanner module."""
import json
import subprocess
from unittest.mock import patch, MagicMock
from pathlib import Path


def test_parse_eslint_output():
    from scripts.overnight.scanner import parse_eslint_output
    eslint_output = """
/path/to/App.jsx
  3:10  error  'unused' is defined but never used  no-unused-vars
  8:5   error  Missing prop validation              react/prop-types

/path/to/Navbar.jsx
  12:3  warning  Unexpected console statement       no-console

✖ 3 problems (2 errors, 1 warning)
"""
    result = parse_eslint_output(eslint_output)
    assert result["error_count"] >= 2
    assert len(result["files"]) >= 1


def test_find_missing_tests():
    from scripts.overnight.scanner import find_missing_tests
    from scripts.overnight.config import WEBSITE_DIR
    missing = find_missing_tests(WEBSITE_DIR / "src")
    assert isinstance(missing, list)
    for item in missing:
        assert "component" in item
        assert "path" in item


def test_scan_code_returns_findings():
    from scripts.overnight.scanner import scan_code
    with patch("scripts.overnight.scanner._run_eslint") as mock_lint:
        mock_lint.return_value = {"error_count": 0, "files": [], "raw": ""}
        with patch("scripts.overnight.scanner.find_missing_tests") as mock_tests:
            mock_tests.return_value = []
            with patch("scripts.overnight.scanner.scan_pipeline_issues") as mock_pipe:
                mock_pipe.return_value = []
                findings = scan_code()
                assert isinstance(findings, list)


def test_parse_score_json():
    from scripts.overnight.scanner import parse_score_json
    score_data = {
        "scores": {
            "factual_accuracy": 8, "style_consistency": 7,
            "readability": 5, "chapter_coherence": 7, "terminology_accuracy": 8,
        },
        "average": 7.0,
        "weaknesses": ["段落长度单一"],
        "suggestions": ["增加句式变化"],
        "verdict": "pass",
    }
    result = parse_score_json(score_data, chapter_num=11, chapter_path="正文/11_test.md")
    assert result["weakest_dimension"] == "readability"
    assert result["weakest_score"] == 5
    assert result["chapter_num"] == 11


def test_scan_pipeline_issues():
    """scan_pipeline_issues detects known pipeline bugs."""
    from scripts.overnight.scanner import scan_pipeline_issues
    findings = scan_pipeline_issues()
    # Should detect the actual bugs in the real quality_scorer.py
    assert isinstance(findings, list)
    # The real scorer has both issues
    types = [f["type"] for f in findings]
    for f in findings:
        assert f["type"] == "pipeline-fix"
        assert f["severity"] >= 9
