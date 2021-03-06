# Copyright (C) 2019 Leiden University Medical Center
# This file is part of git-synchronizer
#
# git-synchronizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# git-synchronizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with git-synchronizer.  If not, see <https://www.gnu.org/licenses/

import tempfile
from pathlib import Path

import git

from git_synchronizer.git_synchronizer import GitRepo

import pytest

from . import clone_this_repo, empty_repo


@pytest.fixture()
def git_repository():
    clone_dir = Path(str(tempfile.mkdtemp(prefix="clone_dir"))) / Path(
        "git-synchronizer.git")

    git_repo = GitRepo(main_url=list(clone_this_repo().remote().urls)[0],
                       mirror_urls=[empty_repo().working_dir,
                                    empty_repo().working_dir],
                       repo_dir=clone_dir)
    return git_repo


def test_clone(git_repository):
    git_repo = git_repository
    assert not git_repo.repo_dir.exists()
    git_repo.clone()
    assert git_repo.repo_dir.exists()


def test_remotes():
    clone_dir = Path(str(tempfile.mkdtemp(prefix="clone_dir"))) / Path(
        "git-synchronizer.git")
    mirror_url_one = empty_repo().working_dir
    mirror_url_two = empty_repo().working_dir
    git_repo = GitRepo(main_url=list(clone_this_repo().remote().urls)[0],
                       mirror_urls=[mirror_url_one, mirror_url_two],
                       repo_dir=clone_dir)
    git_repo.clone()
    assert mirror_url_one in [list(remote.urls)[0] for remote in
                              git_repo.mirrors]
    assert mirror_url_two in [list(remote.urls)[0] for remote in
                              git_repo.mirrors]


def test_remotes_existing(git_repository):
    git_repository.clone()
    git_repo = GitRepo(list(git_repository.repo.remote().urls)[0],
                       repo_dir=Path(git_repository.repo.working_dir))
    assert len(git_repo.mirrors) == 2

# Will fail on travis due to git push failing.
@pytest.mark.xfail
def test_mirror(git_repository):
    git_repo = git_repository
    git_repo.mirror()
    for mirror in git_repo.mirrors:
        mirror_repo = git.Repo(list(mirror.urls)[0])
        print(git_repo.repo_dir)
        print(mirror_repo.working_dir)
        assert mirror_repo.branches == git_repo.repo.branches
        assert mirror_repo.tags == git_repo.repo.tags
