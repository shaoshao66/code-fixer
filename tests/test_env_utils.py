from __future__ import annotations

import os
import subprocess

import pytest

from codefixer.run.hooks.open_pr import _remove_triple_backticks, format_trajectory_markdown
from codefixer.utils.github import (
    InvalidGithubURL,
    _get_associated_commit_urls,
    _is_github_issue_url,
    _is_github_repo_url,
    _parse_gh_issue_url,
    _parse_gh_repo_url,
)


def test_format_trajectory_markdown(test_trajectory):
    formatted = format_trajectory_markdown(test_trajectory["trajectory"])
    assert formatted.startswith("<details>")
    assert formatted.endswith("</details>")


def test_remove_triple_backticks():
    assert _remove_triple_backticks("```") == ""


def test_is_github_repo_url():
    assert _is_github_repo_url("https://github.com/Code-Fixer/Code-Fixer")
    assert _is_github_repo_url("https://github.com/Code-Fixer/Code-Fixer/anything")
    assert _is_github_repo_url("github.com/Code-Fixer/Code-Fixer/anything")
    assert not _is_github_repo_url("")
    assert not _is_github_repo_url("/path/to/file")


def test_parse_gh_repo_url():
    assert _parse_gh_repo_url("https://github.com/Code-Fixer/Code-Fixer") == ("Code-Fixer", "Code-Fixer")
    assert _parse_gh_repo_url("github.com/Code-Fixer/Code-Fixer") == ("Code-Fixer", "Code-Fixer")
    assert _parse_gh_repo_url("github.com/Code-Fixer/Code-Fixer/asdfjsdfg") == ("Code-Fixer", "Code-Fixer")
    assert _parse_gh_repo_url("git@github.com/Code-Fixer/Code-Fixer/asdfjsdfg") == ("Code-Fixer", "Code-Fixer")
    assert _parse_gh_repo_url("https://github.com/Code-Fixer/Code-Fixer.git") == ("Code-Fixer", "Code-Fixer")
    assert _parse_gh_repo_url("github.com/Code-Fixer/Code-Fixer.git") == ("Code-Fixer", "Code-Fixer")
    assert _parse_gh_repo_url("https://github.com/Code-Fixer/Code-Fixer?ref=main") == ("Code-Fixer", "Code-Fixer")
    assert _parse_gh_repo_url("https://github.com/Code-Fixer/Code-Fixer#readme") == ("Code-Fixer", "Code-Fixer")
    assert _parse_gh_repo_url("https://github.com/Code-Fixer/Code-Fixer.git?ref=main") == ("Code-Fixer", "Code-Fixer")


def test_parse_gh_repo_url_fails():
    with pytest.raises(InvalidGithubURL, match="repository URL"):
        _parse_gh_repo_url("adfkj;lasdfl;kj")
    with pytest.raises(InvalidGithubURL):
        _parse_gh_repo_url("github.com/")
    with pytest.raises(InvalidGithubURL):
        _parse_gh_repo_url("github.com//a/")


def test_parse_gh_issue_url():
    url = "https://github.com/Code-Fixer/Code-Fixer/issues/43"
    owner, repo, no = _parse_gh_issue_url(url)
    assert owner == "Code-Fixer"
    assert repo == "Code-Fixer"
    assert no == "43"


def test_parse_gh_issue_url_fails():
    with pytest.raises(InvalidGithubURL):
        _parse_gh_issue_url("https://github.com/a/b")
    with pytest.raises(InvalidGithubURL):
        _parse_gh_issue_url("https://github.com/a/b////")


def test_is_from_github_url():
    assert not _is_github_issue_url("")
    assert _is_github_issue_url("https://github.com/Code-Fixer/Code-Fixer/issues/43")


def test_get_associated_commit_urls():
    assoc = _get_associated_commit_urls(
        org="Code-Fixer",
        repo="Code-Fixer",
        issue_number="41",
        token=os.environ.get("GITHUB_TOKEN", ""),
    )
    assert len(assoc) > 0


def clone_repo(tmp_path, repo_url):
    cmd = [
        "git",
        "clone",
        repo_url,
    ]
    subprocess.run(cmd, check=True, cwd=tmp_path)
