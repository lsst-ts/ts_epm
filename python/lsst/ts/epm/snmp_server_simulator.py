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

__all__ = ["SnmpServerSimulator", "SIMULATED_SYS_DESCR"]

import logging
import random
import string
import typing

from pysnmp.hlapi import (
    CommunityData,
    ContextData,
    Integer,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
)
from pysnmp.proto.rfc1155 import ObjectName
from pysnmp.proto.rfc1902 import OctetString

from .mib_tree_holder import MibTreeHolder
from .utils import TelemetryItemType

SIMULATED_SYS_DESCR = "SnmpServerSimulator"


class SnmpServerSimulator:
    """SNMP server simulator."""

    def __init__(self, log: logging.Logger) -> None:
        self.log = log.getChild(type(self).__name__)
        self.mib_tree_holder = MibTreeHolder()
        self.SYS_DESCR = [
            (
                ObjectName(value=self.mib_tree_holder.mib_tree["sysDescr"].oid + ".0"),
                OctetString(value=SIMULATED_SYS_DESCR),
            )
        ]

    def snmp_cmd(
        self,
        snmp_engine: SnmpEngine,
        auth_data: CommunityData,
        transport_target: UdpTransportTarget,
        context_data: ContextData,
        *var_binds: typing.Any,
        **options: typing.Any,
    ) -> typing.Iterator:
        """Handle all SNMP commands."""

        assert snmp_engine is not None
        assert auth_data is not None
        assert transport_target is not None
        assert context_data is not None
        assert len(options) == 2

        # The pysnmp API is a mess so we need to access "private" members to
        # get the info we want. The noinspection comments keep PyCharm happy.
        assert isinstance(var_binds[0], ObjectType)
        # noinspection PyProtectedMember
        assert isinstance(var_binds[0]._ObjectType__args[0], ObjectIdentity)
        # noinspection PyProtectedMember
        object_identity = var_binds[0]._ObjectType__args[0]._ObjectIdentity__args[0]

        if object_identity == self.mib_tree_holder.mib_tree["sysDescr"].oid:
            # Handle the getCmd call for the system description.
            return iter([[None, Integer(0), Integer(0), self.SYS_DESCR]])
        else:
            oid_branch = [
                t
                for t in self.mib_tree_holder.mib_tree
                if self.mib_tree_holder.mib_tree[t].oid == object_identity
            ]
            if len(oid_branch) != 1:
                return iter(
                    [[f"Unknown OID {object_identity}.", Integer(0), Integer(0), ""]]
                )

        snmp_items = self.generate_snmp_values(object_identity)
        return iter(snmp_items)

    def generate_snmp_values(self, object_identity: str) -> list[list]:
        snmp_items: list[list] = []
        for elt in self.mib_tree_holder.mib_tree:
            if self.mib_tree_holder.mib_tree[elt].oid.startswith(object_identity):
                try:
                    match TelemetryItemType[elt]:
                        case "int":
                            value = Integer(random.randrange(0, 100, 1))
                        case "float":
                            # SNMP doesn't have floats. Instead an int needs to
                            # be used and that needs to be interpreted as a
                            # float by the reader.
                            value = Integer(random.randrange(100, 1000, 1))
                        case "string":
                            value = OctetString(
                                value="".join(
                                    random.choices(
                                        string.ascii_uppercase + string.digits, k=20
                                    )
                                )
                            )
                        case _:
                            value = Integer(0)
                            self.log.error(
                                f"Unknown telemetry item type {TelemetryItemType[elt]} for {elt=}"
                            )
                    # TODO DM-44577 Handle list items correctly.
                    # Any single value OID ends in ".0" in the SNMP response.
                    # Any multiple value ends in # ".1", ".2", etc. We only
                    # regard ".1" for now.
                    suffix = ".0"
                    parent = self.mib_tree_holder.mib_tree[elt].parent
                    assert parent is not None
                    if parent.index:
                        suffix = ".1"
                    snmp_items.append(
                        [
                            None,
                            Integer(0),
                            Integer(0),
                            [
                                (
                                    ObjectName(
                                        value=self.mib_tree_holder.mib_tree[elt].oid
                                        + suffix
                                    ),
                                    value,
                                )
                            ],
                        ]
                    )
                except KeyError:
                    # Deliberately ignored.
                    pass
        return snmp_items
