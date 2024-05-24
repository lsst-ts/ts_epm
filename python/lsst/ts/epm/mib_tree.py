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

__all__ = ["mib_tree"]

import logging
import pathlib
import re

from .utils import MibTreeElement, MibTreeElementType

OBJECT_IDENTIFIER = r"^(\w+) +OBJECT IDENTIFIER +::= \{ ?(\w+) (\d+) ?\}$"
OBJECT_TYPE = r"^(\w+) OBJECT-TYPE$"
MIB_OID = r"^::= ?{ ?(\w+) +(\d+) ?}$"
DESCRIPTION = "DESCRIPTION"

DATA_DIR = pathlib.Path(__file__).parent / "data"

_line_num = 0

log = logging.getLogger("MIB")


def _add_default_elements() -> None:
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
        oid="2",
        parent=snmp,
        type=MibTreeElementType.BRANCH,
    )
    sys_descr = MibTreeElement(
        name="sysDescr",
        description="System Description.",
        oid="1.1.1",
        parent=system,
        type=MibTreeElementType.BRANCH,
    )
    private = MibTreeElement(
        name="private",
        description="private",
        oid="4",
        parent=snmp,
        type=MibTreeElementType.BRANCH,
    )
    enterprises = MibTreeElement(
        name="enterprises",
        description="enterprises",
        oid="1",
        parent=private,
        type=MibTreeElementType.BRANCH,
    )
    eaton = MibTreeElement(
        name="eaton",
        description="eaton",
        oid="534",
        parent=enterprises,
        type=MibTreeElementType.BRANCH,
    )
    xups = MibTreeElement(
        name="xups",
        description="xups",
        oid="1",
        parent=eaton,
        type=MibTreeElementType.BRANCH,
    )
    mib_tree[snmp.name] = snmp
    mib_tree[system.name] = system
    mib_tree[sys_descr.name] = sys_descr
    mib_tree[private.name] = private
    mib_tree[enterprises.name] = enterprises
    mib_tree[eaton.name] = eaton
    mib_tree[xups.name] = xups


def _add_mib_elements() -> None:
    global _line_num
    for filename in DATA_DIR.glob("*.mib"):
        with open(filename) as f:
            lines = f.readlines()

        for _line_num in range(len(lines)):
            line = lines[_line_num].strip()
            obj_id_match = re.match(OBJECT_IDENTIFIER, line)
            obj_type_match = re.match(OBJECT_TYPE, line)
            if obj_id_match:
                parent_name = obj_id_match.group(2)
                parent: MibTreeElement | None = _get_parent(parent_name)
                name = obj_id_match.group(1)
                if name == "synaccess":
                    name = "pdu"
                if name == "schneiderElectric":
                    name = "scheiderPm5xxx"
                mib_tree[name] = MibTreeElement(
                    name=name,
                    description=obj_id_match.group(1),
                    oid=obj_id_match.group(3),
                    parent=parent,
                    type=MibTreeElementType.BRANCH,
                )
            elif obj_type_match:
                _process_obj_type(lines, line, obj_type_match)


def _get_parent(parent_name: str) -> MibTreeElement | None:
    parent: MibTreeElement | None = None
    if parent_name == "xupsMIB":
        parent_name = "xups"
    elif parent_name == "synSys":
        parent_name = "pdu"
    elif parent_name == "schneiderElectric":
        parent_name = "scheiderPm5xxx"
    if parent_name in mib_tree:
        parent = mib_tree[parent_name]
    else:
        log.debug(f"WOUTER {parent_name=!r} not found.")
    return parent


def _process_obj_type(lines: list[str], line: str, obj_type_match: re.Match) -> None:
    global _line_num

    name = obj_type_match.group(1)

    description = ""
    while DESCRIPTION not in line:
        _line_num += 1
        line = lines[_line_num].strip()
    # The line containing "::=" always follows the description in any
    # MIB file.
    while "::=" not in line:
        description += line.replace(DESCRIPTION, "").strip()
        if description != "":
            description += " "
        _line_num += 1
        line = lines[_line_num].strip()
    # Remove multiple spaces and strip white space.
    description = re.sub(r" +", " ", description).replace('"', "").strip()

    oid_match = re.match(MIB_OID, line)
    assert oid_match is not None
    parent_name = oid_match.group(1)
    parent = mib_tree[parent_name]
    oid = oid_match.group(2)

    mib_tree[name] = MibTreeElement(
        name=name,
        description=description,
        oid=oid,
        parent=parent,
        type=MibTreeElementType.LEAF,
    )


# Defined this way, the "mib_tree" attribute becomes available as a "singleton"
# for all code that imports it.
mib_tree: dict[str, MibTreeElement] = {}
_add_default_elements()
_add_mib_elements()
