import os

import pytest
from click.testing import Result

from gitrack import helpers, exceptions


class TestInit:
    def test_init(self, repo_dir, cmd):
        assert helpers.is_repo_initialized(repo_dir) is False
        assert (repo_dir / '.git' / 'hooks' / 'post-commit').exists() is False
        assert (repo_dir / '.git' / 'hooks' / 'post-commit.gitrack').exists() is False

        result = cmd('init', repo_dir=repo_dir, inited=False)  # type: Result
        assert result.exit_code == 0

        assert helpers.is_repo_initialized(repo_dir) is True
        assert (repo_dir / '.git' / 'hooks' / 'post-commit').exists()
        assert (repo_dir / '.git' / 'hooks' / 'post-commit.gitrack').exists()

    def test_init_without_hooks(self, repo_dir, cmd):
        assert helpers.is_repo_initialized(repo_dir) is False
        assert (repo_dir / '.git' / 'hooks' / 'post-commit').exists() is False
        assert (repo_dir / '.git' / 'hooks' / 'post-commit.gitrack').exists() is False

        result = cmd('init --no-hook', repo_dir=repo_dir, inited=False)  # type: Result
        assert result.exit_code == 0

        assert helpers.is_repo_initialized(repo_dir) is True
        assert (repo_dir / '.git' / 'hooks' / 'post-commit').exists() is False
        assert (repo_dir / '.git' / 'hooks' / 'post-commit.gitrack').exists() is False

    def test_abort_already_initied(self, inited_repo_dir, cmd):
        assert helpers.is_repo_initialized(inited_repo_dir) is True

        with pytest.raises(exceptions.InitializedRepoException):
            cmd('init', repo_dir=inited_repo_dir, inited=False)  # type: Result

    def test_check(self, cmd):
        result = cmd('init --check', inited=False)  # type: Result
        assert result.exit_code == 2

        result = cmd('init --check', inited=True)  # type: Result
        assert result.exit_code == 0

    def test_hook_install(self, repo_dir, cmd):
        assert helpers.is_repo_initialized(repo_dir) is False
        assert (repo_dir / '.git' / 'hooks' / 'post-commit').exists() is False
        assert (repo_dir / '.git' / 'hooks' / 'post-commit.gitrack').exists() is False

        result = cmd('init --install-hook', repo_dir=repo_dir, inited=False)  # type: Result
        assert result.exit_code == 0

        assert helpers.is_repo_initialized(repo_dir) is False
        assert (repo_dir / '.git' / 'hooks' / 'post-commit').exists() is True
        assert (repo_dir / '.git' / 'hooks' / 'post-commit.gitrack').exists() is True


