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

__all__ = ["MibTreeHolder"]

import logging
import pathlib
import re

from .utils import MibTreeElement, MibTreeElementType

OBJECT_IDENTIFIER = r"^(\w+) +OBJECT IDENTIFIER +::= \{ ?(\w+) (\d+) ?\}$"
OBJECT_TYPE = r"^(\w+) OBJECT-TYPE$"
MIB_OID = r"^::= ?{ ?(\w+) +(\d+) ?}$"
DESCRIPTION = "DESCRIPTION"
INDEX = r"INDEX +\{ ?(\w+) ?\}"

DATA_DIR = pathlib.Path(__file__).parent / "data"


class MibTreeHolder:
    """Holder of information in an MIB tree.

    MIB stands for Management Information Base and holds the information for
    managing the entities in a communication network, in this case SNMP or
    Simple Network Management Protocol. The information can be represented as a
    tree, hence the name of the class.
    """

    def __init__(self) -> None:
        self.log = logging.getLogger(type(self).__name__)
        self._line_num = 0
        self.mib_tree: dict[str, MibTreeElement] = {}
        self._add_default_elements()
        self._add_mib_elements()

    def _add_default_elements(self) -> None:
        """Add the default MIB elements.

        The default elements are the root, system and enterprises branches as
        well as a branch for Eaton PDU devices since their MIB file has a
        deviating syntax."""
        snmp = MibTreeElement(
            name="snmp",
            description="snmp",
            oid="1.3.6.1",
            parent=None,
            type=MibTreeElementType.BRANCH,
        )
        system = MibTreeElement(
            name="system",
            description="system",
            oid="1.3.6.1.2",
            parent=snmp,
            type=MibTreeElementType.BRANCH,
        )
        sys_descr = MibTreeElement(
            name="sysDescr",
            description="System Description.",
            oid="1.3.6.1.2.1.1.1",
            parent=system,
            type=MibTreeElementType.BRANCH,
        )
        private = MibTreeElement(
            name="private",
            description="private",
            oid="1.3.6.1.4",
            parent=snmp,
            type=MibTreeElementType.BRANCH,
        )
        enterprises = MibTreeElement(
            name="enterprises",
            description="enterprises",
            oid="1.3.6.1.4.1",
            parent=private,
            type=MibTreeElementType.BRANCH,
        )
        eaton = MibTreeElement(
            name="eaton",
            description="eaton",
            oid="1.3.6.1.4.1.534",
            parent=enterprises,
            type=MibTreeElementType.BRANCH,
        )
        xups = MibTreeElement(
            name="xups",
            description="xups",
            oid="1.3.6.1.4.1.534.1",
            parent=eaton,
            type=MibTreeElementType.BRANCH,
        )
        self.mib_tree[snmp.name] = snmp
        self.mib_tree[system.name] = system
        self.mib_tree[sys_descr.name] = sys_descr
        self.mib_tree[private.name] = private
        self.mib_tree[enterprises.name] = enterprises
        self.mib_tree[eaton.name] = eaton
        self.mib_tree[xups.name] = xups

    def _add_mib_elements(self) -> None:
        """Loop over the MIB files and add their contents as a tree
        structure."""
        for filename in DATA_DIR.glob("*.mib"):
            with open(filename) as f:
                lines = f.readlines()

            for self._line_num in range(len(lines)):
                line = lines[self._line_num].strip()
                obj_id_match = re.match(OBJECT_IDENTIFIER, line)
                obj_type_match = re.match(OBJECT_TYPE, line)
                if obj_id_match:
                    parent_name = obj_id_match.group(2)
                    parent: MibTreeElement | None = self._get_parent(parent_name)
                    assert parent is not None
                    name = obj_id_match.group(1)
                    if name == "synaccess":
                        name = "pdu"
                    if name == "schneiderElectric":
                        name = "scheiderPm5xxx"
                    self.mib_tree[name] = MibTreeElement(
                        name=name,
                        description=obj_id_match.group(1),
                        oid=f"{parent.oid}.{obj_id_match.group(3)}",
                        parent=parent,
                        type=MibTreeElementType.BRANCH,
                    )
                elif obj_type_match:
                    self._process_obj_type(lines, line, obj_type_match)

    def _get_parent(self, parent_name: str) -> MibTreeElement | None:
        """Get the MIB parent branch for the fiven parent name.

        Parameters
        ----------
        parent_name : `str`
            The name of the parent to get.
        """
        parent: MibTreeElement | None = None
        if parent_name == "xupsMIB":
            parent_name = "xups"
        elif parent_name == "synSys":
            parent_name = "pdu"
        elif parent_name == "schneiderElectric":
            parent_name = "scheiderPm5xxx"
        if parent_name in self.mib_tree:
            parent = self.mib_tree[parent_name]
        else:
            self.log.debug(f"{parent_name=!r} not found.")
        return parent

    def _process_obj_type(
        self, lines: list[str], line: str, obj_type_match: re.Match
    ) -> None:
        """Utility method to process OBJECT_TYPE entries.

        Parameters
        ----------
        lines : `list`[`str`]
            The lines as read from an MIB file.
        line : `str`
            The current line that is processed.
        obj_type_match : `re.Match`
            Regex Match object used to look up the name of the object type.
        """
        name = obj_type_match.group(1)

        description = ""
        while DESCRIPTION not in line:
            self._line_num += 1
            line = lines[self._line_num].strip()
        while "::=" not in line and "INDEX " not in line:
            description += line.replace(DESCRIPTION, "").strip()
            if description != "":
                description += " "
            self._line_num += 1
            line = lines[self._line_num].strip()
        # Remove multiple spaces and strip white space.
        description = re.sub(r" +", " ", description).replace('"', "").strip()

        index: str | None = None
        if "INDEX " in line:
            index_match = re.match(INDEX, line)
            if index_match:
                index = index_match.group(1)
                self._line_num += 1
                line = lines[self._line_num].strip()

        oid_match = re.match(MIB_OID, line)
        assert oid_match is not None
        parent_name = oid_match.group(1)
        parent = self.mib_tree[parent_name]
        oid = oid_match.group(2)

        self.mib_tree[name] = MibTreeElement(
            name=name,
            description=description,
            oid=f"{parent.oid}.{oid}",
            parent=parent,
            type=MibTreeElementType.LEAF,
            index=index,
        )
