#!/usr/bin/env python3

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

import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clone-dir", type=Path,
                        help="Where repositories should be cloned on the "
                             "local machine.")
    parser.add_argument("--config", type=Path,
                        help="The configuration file")
    return parser


class GitRepo(object):
    def __init__(self,
                 main_url: str,
                 mirror_urls: List[str],
                 repo_dir: Path):
        self.main_url = main_url
        self.mirror_urls = mirror_urls
        self.repo_dir = repo_dir

    def exists(self):
        return (self.repo_dir / Path(".git")).exists()

    def clone_mirror(self):
        if not self.exists():
            subprocess.run(args=["git", "clone", "--mirror", self.main_url, self.repo_dir.absolute()])

    def fetch(self):
        subprocess.run(args=["git", "-C", self.repo_dir.absolute(), "fetch"])

    def push_to_mirrors(self):
        for mirror_url in self.mirror_urls:
            subprocess.run(args=["git", "-C", self.repo_dir.absolute(), "push", "--all", mirror_url])
            subprocess.run(args=["git", "-C", self.repo_dir.absolute(), "push", "--tags", mirror_url])


def parse_config(config: Path) -> List[Tuple[str, List[str]]]:
    with config.open('rt') as config_h:
        config_lines = config_h.readlines()
    return [
        (urls.split("\t")[0], urls.split("\t")[1:])
        for urls in config_lines]


def main():
    pass


if __name__ == "__main__":
    main()