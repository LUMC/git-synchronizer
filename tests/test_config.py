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

from pathlib import Path

from git_synchronizer.git_synchronizer import parse_config

EXAMPLE_CONFIG = Path(__file__).parent.parent / Path("example_config.tsv")


def test_config_parsing():
    config = parse_config(EXAMPLE_CONFIG)
    assert len(config) == 2
    assert config[0] == ("https://example.com/examples/example.git",
                         ["git@mygit.com:/examples/example.git"])
    assert config[1] == ("https://example.com/examples/example2.git",
                         ["git@mygit.com:/examples/example2.git",
                          "git@myothergit.com/example/example2.git"])
