# This file is part of ts_epm.
#
# Developed for the Vera Rubin Observatory Telescope and Site Systems.
# This product includes software developed by the Vera Rubin Observatory
# Project (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

__all__ = ["MibTreeElement", "MibTreeElementType"]

import enum
from dataclasses import dataclass


@dataclass
class MibTreeElement:
    """MIB Tree Element.

    A Tree Element can either be a BRANCH or a LEAF.
    """

    name: str
    description: str
    oid: str
    parent: MibTreeElement | None
    type: str

    def __repr__(self) -> str:
        return f"{'' if self.parent is None else str(self.parent) + '.'}{self.oid}"


class MibTreeElementType(enum.StrEnum):
    """MIB Tree Element Type."""

    BRANCH = "BRANCH"
    LEAF = "LEAF"
